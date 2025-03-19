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
              param_bounds: Optional[Tuple] = None) -> pd.DataFrame:
    """
    Fit a volatility model to market data.

    Parameters:
    - option_chain: DataFrame with market data
    - model_name: Type of model to fit (default: 'svi')
    - initial_params: Optional initial parameters for optimization (default: model's defaults)
    - param_bounds: Optional parameter bounds for optimization (default: model's defaults)

    Returns:
    - DataFrame with all fit results and performance metrics as columns, maturity_names as index
    """
    if model_name.lower() != 'svi':
        raise VolyError(f"Model type '{model_name}' is not supported. Currently only 'svi' is available.")

    # Use defaults if not provided
    initial_params = initial_params or SVIModel.DEFAULT_INITIAL_PARAMS
    param_bounds = param_bounds or SVIModel.DEFAULT_PARAM_BOUNDS

    # Define column names and their data types
    column_dtypes = {
        's': float,
        'u': float,
        'maturity_date': 'datetime64[ns]',
        'dtm': float,
        'ytm': float,
        'a': float,
        'b': float,
        'rho': float,
        'm': float,
        'sigma': float,
        'nu': float,
        'psi': float,
        'p': float,
        'c': float,
        'nu_tilde': float,
        'oi': float,
        'volume': float,
        'r': float,
        'fit_success': bool,
        'cost': float,
        'optimality': float,
        'rmse': float,
        'mae': float,
        'r2': float,
        'max_error': float,
        'n_points': int
    }

    # Get unique maturities and sort them
    unique_ytms = sorted(option_chain['ytm'].unique())
    maturity_names = [option_chain[option_chain['ytm'] == ytm]['maturity_name'].iloc[0] for ytm in unique_ytms]

    # Store results in a dictionary first
    results_data = {col: [] for col in column_dtypes.keys()}

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
        r = maturity_data['interest_rate'].iloc[0] if 'interest_rate' in maturity_data.columns else 0

        # Calculate Jump-Wing parameters
        nu, psi, p, c, nu_tilde = SVIModel.raw_to_jw_params(a, b, sigma, rho, m, ytm)

        # Store values in the results dictionary with proper types
        results_data['s'].append(float(s))
        results_data['u'].append(float(u))
        results_data['maturity_date'].append(maturity_data['maturity_date'].iloc[0])
        results_data['dtm'].append(float(dtm))
        results_data['ytm'].append(float(ytm))
        results_data['a'].append(float(a))
        results_data['b'].append(float(b))
        results_data['rho'].append(float(rho))
        results_data['m'].append(float(m))
        results_data['sigma'].append(float(sigma))
        results_data['nu'].append(float(nu))
        results_data['psi'].append(float(psi))
        results_data['p'].append(float(p))
        results_data['c'].append(float(c))
        results_data['nu_tilde'].append(float(nu_tilde))
        results_data['oi'].append(float(oi))
        results_data['volume'].append(float(volume))
        results_data['r'].append(float(r))
        results_data['fit_success'].append(bool(result.success))
        results_data['cost'].append(float(result.cost))
        results_data['optimality'].append(float(result.optimality))
        results_data['rmse'].append(float(rmse))
        results_data['mae'].append(float(mae))
        results_data['r2'].append(float(r2))
        results_data['max_error'].append(float(max_error))
        results_data['n_points'].append(int(len(maturity_data)))

        # Log result
        status = f'{GREEN}SUCCESS{RESET}' if result.success else f'{RED}FAILED{RESET}'
        logger.info(f'Optimization for {maturity_name}: {status}')
        logger.info('-------------------------------------')

    # Create DataFrame with proper types
    results_df = pd.DataFrame(results_data, index=maturity_names)

    # Convert columns to appropriate types
    for col, dtype in column_dtypes.items():
        if col in results_df.columns:
            try:
                results_df[col] = results_df[col].astype(dtype)
            except (ValueError, TypeError) as e:
                logger.warning(f"Could not convert column {col} to {dtype}: {e}")

    return results_df


@catch_exception
def get_iv_surface(fit_results: pd.DataFrame,
                   log_moneyness_params: Tuple[float, float, int] = (-1.5, 1.5, 1000),
                   return_domain: str = 'log_moneyness') -> Tuple[Dict[str, np.ndarray], Dict[str, np.ndarray]]:
    """
    Generate implied volatility surface using optimized SVI parameters.

    Parameters:
    - fit_results: DataFrame from fit_model() with maturity names as index
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

    # Process each maturity
    for maturity in fit_results.index:
        # Calculate SVI total implied variance and convert to IV
        params = [
            fit_results.loc[maturity, 'a'],
            fit_results.loc[maturity, 'b'],
            fit_results.loc[maturity, 'sigma'],
            fit_results.loc[maturity, 'rho'],
            fit_results.loc[maturity, 'm']
        ]
        ytm = fit_results.loc[maturity, 'ytm']

        # Calculate implied volatility
        w_svi = np.array([SVIModel.svi(x, *params) for x in log_moneyness_array])
        iv_array = np.sqrt(w_svi / ytm)
        iv_surface[maturity] = iv_array

        # Calculate x domain for this maturity
        x_surface[maturity] = get_x_domain(
            log_moneyness_params=log_moneyness_params,
            return_domain=return_domain,
            s=fit_results.loc[maturity, 's'],
            r=fit_results.loc[maturity, 'r'],
            iv_array=iv_array,
            ytm=ytm
        )

    return iv_surface, x_surface
