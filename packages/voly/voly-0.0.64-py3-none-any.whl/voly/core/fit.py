"""
Model fitting and calibration module for the Voly package.

This module handles fitting volatility models to market data and
calculating fitting statistics.
"""

import numpy as np
import pandas as pd
from typing import List, Tuple, Dict, Optional, Union, Any
from scipy.optimize import least_squares
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from voly.utils.logger import logger, catch_exception
from voly.formulas import get_x_domain
from voly.exceptions import VolyError
from voly.models import SVIModel
import warnings

warnings.filterwarnings("ignore")


@catch_exception
def calculate_residuals(params: List[float], ytm: float, option_chain: pd.DataFrame,
                        model: Any = SVIModel) -> np.ndarray:
    """Calculate residuals between market and model implied volatilities."""
    maturity_data = option_chain[option_chain['ytm'] == ytm]
    w = np.array([model.svi(x, *params) for x in maturity_data['log_moneyness']])
    iv_actual = maturity_data['mark_iv'].values
    return iv_actual - np.sqrt(w / ytm)


@catch_exception
def fit_model(option_chain: pd.DataFrame,
              model_name: str = 'svi',
              initial_params: Optional[List[float]] = None,
              param_bounds: Optional[Tuple] = None) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Fit a volatility model to market data.

    Returns:
    - Tuple of (fit_results_df, fit_performance_df)
    """
    if model_name.lower() != 'svi':
        raise VolyError(f"Model type '{model_name}' is not supported. Currently only 'svi' is available.")

    # Use defaults if not provided
    initial_params = initial_params or SVIModel.DEFAULT_INITIAL_PARAMS
    param_bounds = param_bounds or SVIModel.DEFAULT_PARAM_BOUNDS

    # Define indices for result DataFrames
    results_index = ['s', 'u', 'maturity_date', 'dtm', 'ytm',
                     'a', 'b', 'sigma', 'rho', 'm',
                     'nu', 'psi', 'p', 'c', 'nu_tilde',
                     'oi', 'volume', 'r']

    performance_index = ['fit_success', 'cost', 'optimality',
                         'rmse', 'mae', 'r2', 'max_error', 'n_points']

    # Get unique maturities and sort them
    unique_ytms = sorted(option_chain['ytm'].unique())
    maturity_names = [option_chain[option_chain['ytm'] == ytm]['maturity_name'].iloc[0] for ytm in unique_ytms]

    # Create empty DataFrames
    fit_results_df = pd.DataFrame(index=results_index, columns=maturity_names)
    fit_performance_df = pd.DataFrame(index=performance_index, columns=maturity_names)

    # ANSI color codes for terminal output
    GREEN, RED, RESET = '\033[32m', '\033[31m', '\033[0m'

    for ytm in unique_ytms:
        # Get data for this maturity
        maturity_data = option_chain[option_chain['ytm'] == ytm]
        maturity_name = maturity_data['maturity_name'].iloc[0]
        dtm = maturity_data['dtm'].iloc[0]

        logger.info(f"Optimizing for {maturity_name}...")

        # Optimize SVI parameters
        try:
            result = least_squares(
                calculate_residuals,
                initial_params,
                args=(ytm, option_chain, SVIModel),
                bounds=param_bounds,
                max_nfev=1000
            )
        except Exception as e:
            raise VolyError(f"Optimization failed for {maturity_name}: {str(e)}")

        # Extract raw parameters
        a, b, sigma, rho, m = result.x

        # Calculate model predictions for statistics
        w = np.array([SVIModel.svi(x, *result.x) for x in maturity_data['log_moneyness']])
        iv_model = np.sqrt(w / ytm)
        iv_market = maturity_data['mark_iv'].values

        # Calculate statistics
        rmse = np.sqrt(mean_squared_error(iv_market, iv_model))
        mae = mean_absolute_error(iv_market, iv_model)
        r2 = r2_score(iv_market, iv_model)
        max_error = np.max(np.abs(iv_market - iv_model))

        # Get or calculate additional required data
        s = maturity_data['index_price'].iloc[0]
        u = maturity_data['underlying_price'].iloc[0]

        # Aggregate open interest and volume
        oi = maturity_data['open_interest'].sum() if 'open_interest' in maturity_data.columns else 0
        volume = maturity_data['volume'].sum() if 'volume' in maturity_data.columns else 0
        r = 0.0

        # Calculate Jump-Wing parameters
        nu, psi, p, c, nu_tilde = SVIModel.raw_to_jw_params(a, b, sigma, rho, m, ytm)

        # Store results
        result_values = [s, u, maturity_data['maturity_date'].iloc[0], dtm, ytm,
                         a, b, rho, m, sigma, nu, psi, p, c, nu_tilde, oi, volume, r]

        for idx, val in zip(results_index, result_values):
            fit_results_df.loc[idx, maturity_name] = val

        # Store performance metrics
        perf_values = [result.success, result.cost, result.optimality,
                       rmse, mae, r2, max_error, len(maturity_data)]

        for idx, val in zip(performance_index, perf_values):
            fit_performance_df.loc[idx, maturity_name] = val

        # Log result
        status = f'{GREEN}SUCCESS{RESET}' if result.success else f'{RED}FAILED{RESET}'
        logger.info(f'Optimization for {maturity_name}: {status}')
        logger.info('-------------------------------------')

    return fit_results_df, fit_performance_df


@catch_exception
def get_iv_surface(fit_results: pd.DataFrame,
                   log_moneyness_params: Tuple[float, float, int] = (-1.5, 1.5, 1000),
                   return_domain: str = 'log_moneyness') -> Tuple[Dict[str, np.ndarray], np.ndarray]:
    """
    Generate implied volatility surface using optimized SVI parameters.

    Parameters:
    - fit_results: DataFrame from fit_model()
    - log_moneyness_params: Tuple of (min, max, num_points) for the moneyness grid
    - return_domain: Domain for x-axis values ('log_moneyness', 'moneyness', 'strikes', 'delta')

    Returns:
    - Tuple of (iv_surface, x_surface)
      iv_surface: Dictionary mapping maturity names to IV arrays
      x_surface: Dictionary mapping maturity names to requested x domain arrays
    """

    # Generate implied volatility surface in log-moneyness domain
    min_m, max_m, num_points = log_moneyness_params
    log_moneyness_array = np.linspace(min_m, max_m, num=num_points)

    iv_surface = {}
    x_surface = {}
    for maturity in fit_results.columns:
        # Calculate SVI total implied variance and convert to IV
        params = [
            fit_results.loc['a', maturity],
            fit_results.loc['b', maturity],
            fit_results.loc['sigma', maturity],
            fit_results.loc['rho', maturity],
            fit_results.loc['m', maturity]
        ]
        ytm = fit_results.loc['ytm', maturity]

        w_svi = np.array([SVIModel.svi(x, *params) for x in log_moneyness_array])
        iv_array = np.sqrt(w_svi / ytm)
        iv_surface[maturity] = iv_array

        x_domain = get_x_domain(
            log_moneyness_params=log_moneyness_params,
            return_domain=return_domain,
            s=fit_results.loc['s', maturity],
            r=fit_results.loc['r', maturity],
            iv_array=iv_array,
            ytm=fit_results.loc['ytm', maturity]
        )

        x_surface[maturity] = x_domain

    return iv_surface, x_surface
