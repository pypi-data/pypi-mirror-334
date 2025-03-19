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
from voly.exceptions import VolyError
from voly.models import SVIModel
import warnings

warnings.filterwarnings("ignore")


@catch_exception
def calculate_residuals(params: List[float],
                        ytm: float,
                        market_data: pd.DataFrame,
                        model: Any = SVIModel) -> np.ndarray:
    """
    Calculate the residuals between market and model implied volatilities.

    Parameters:
    - params: Model parameters (e.g., SVI parameters [a, b, sigma, rho, m])
    - ytm: The time to maturity in years
    - market_data: DataFrame with market data
    - model: Model class to use (default: SVIModel)

    Returns:
    - Array of residuals
    """
    # Filter market data for the specific time to maturity
    maturity_data = market_data[market_data['ytm'] == ytm]

    # Calculate the total implied variance (w) using the model for filtered data
    w = np.array([model.svi(x, *params) for x in maturity_data['log_moneyness']])

    # Extract the actual market implied volatilities
    iv_actual = maturity_data['mark_iv'].values

    # Calculate residuals between market implied volatilities and model predictions
    residuals = iv_actual - np.sqrt(w / ytm)

    return residuals


@catch_exception
def fit_svi_parameters(market_data: pd.DataFrame,
                       initial_params: Optional[List[float]] = None,
                       param_bounds: Optional[Tuple] = None) -> Tuple[pd.DataFrame, Dict[str, Dict]]:
    """
    Fit SVI parameters for all unique expiries in the market data.

    Parameters:
    - market_data: DataFrame with market data
    - initial_params: Initial guess for SVI parameters (default: from SVIModel)
    - param_bounds: Bounds for parameters (default: from SVIModel)

    Returns:
    - Tuple of (fit_performance DataFrame, params_dict)
    """
    # Use defaults if not provided
    if initial_params is None:
        initial_params = SVIModel.DEFAULT_INITIAL_PARAMS

    if param_bounds is None:
        param_bounds = SVIModel.DEFAULT_PARAM_BOUNDS

    # Initialize data for fit performance
    fit_data = {
        'maturity_name': [],
        'dtm': [],
        'ytm': [],
        'fit_success': [],
        'cost': [],
        'optimality': [],
        'rmse': [],
        'mae': [],
        'r2': [],
        'max_error': [],
        'n_point': []
    }

    # Dictionary to store parameters
    params_dict = {}

    # ANSI color codes for terminal output
    GREEN = '\033[32m'
    RED = '\033[31m'
    RESET = '\033[0m'

    # Get unique expiries
    unique_maturities = sorted(market_data['ytm'].unique())

    for ytm in unique_maturities:
        # Get maturity name for reporting
        maturity_data = market_data[market_data['ytm'] == ytm]
        maturity_name = maturity_data['maturity_name'].iloc[0]
        dtm = maturity_data['dtm'].iloc[0]

        logger.info(f"Optimizing for {maturity_name}...")

        # Optimize SVI parameters
        try:
            result = least_squares(
                calculate_residuals,
                initial_params,
                args=(ytm, market_data, SVIModel),
                bounds=param_bounds,
                max_nfev=1000
            )
        except Exception as e:
            raise VolyError(f"Optimization failed for {maturity_name}: {str(e)}")

        # Get parameters
        params = result.x
        params_dict[maturity_name] = {
            'params': params,
            'dtm': dtm,
            'ytm': ytm
        }

        # Calculate model predictions for statistics
        w = np.array([SVIModel.svi(x, *params) for x in maturity_data['log_moneyness']])
        iv_model = np.sqrt(w / ytm)
        iv_market = maturity_data['mark_iv'].values

        # Calculate statistics
        rmse = np.sqrt(mean_squared_error(iv_market, iv_model))
        mae = mean_absolute_error(iv_market, iv_model)
        r2 = r2_score(iv_market, iv_model)
        max_error = np.max(np.abs(iv_market - iv_model))
        num_points = len(maturity_data)

        # Add to fit data
        fit_data['maturity'].append(maturity_name)
        fit_data['dtm'].append(dtm)
        fit_data['ytm'].append(ytm)
        fit_data['fit_success'].append(result.success)
        fit_data['cost'].append(result.cost)
        fit_data['optimality'].append(result.optimality)
        fit_data['rmse'].append(rmse)
        fit_data['mae'].append(mae)
        fit_data['r2'].append(r2)
        fit_data['max_error'].append(max_error)
        fit_data['n_points'].append(num_points)

        if result.success:
            logger.info(f'Optimization for {maturity_name}: {GREEN}SUCCESS{RESET}')
        else:
            logger.warning(f'Optimization for {maturity_name}: {RED}FAILED{RESET}')

        logger.info('-------------------------------------')

    # Create DataFrame with all fit performance data
    fit_performance = pd.DataFrame(fit_data)

    return fit_performance, params_dict


@catch_exception
def create_parameters_matrix(params_dict: Dict[str, Dict]) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Create matrices of optimized parameters for each maturity.
    Uses maturity names as column names.

    Parameters:
    - params_dict: Dictionary of raw parameter results by maturity name

    Returns:
    - Tuple of DataFrames with optimized parameters:
      1. Raw SVI parameters (a, b, sigma, rho, m)
      2. Jump-Wing parameters (nu, psi, p, c, nu_tilde)
    """
    # Get maturity names in order by DTE
    maturity_names = sorted(params_dict.keys(),
                            key=lambda x: params_dict[x]['dtm'])

    # Create DataFrame for raw parameters
    raw_params_matrix = pd.DataFrame(
        columns=maturity_names,
        index=SVIModel.PARAM_NAMES
    )

    # Create DataFrame for JW parameters
    jw_params_matrix = pd.DataFrame(
        columns=maturity_names,
        index=SVIModel.JW_PARAM_NAMES
    )

    # Store YTM and DTM values for reference
    ytm_values = {}
    dtm_values = {}

    # Fill the matrices with optimized parameters
    for maturity_name in maturity_names:
        result = params_dict[maturity_name]

        # Extract raw SVI parameters
        a, b, sigma, rho, m = result['params']
        raw_params_matrix[maturity_name] = [a, b, sigma, rho, m]

        # Get time to maturity
        ytm = result['ytm']
        ytm_values[maturity_name] = ytm
        dtm_values[maturity_name] = result['dtm']

        # Calculate JW parameters
        nu, psi, p, c, nu_tilde = SVIModel.raw_to_jw_params(a, b, sigma, rho, m, ytm)
        jw_params_matrix[maturity_name] = [nu, psi, p, c, nu_tilde]

    # Store YTE and DTE as attributes in all DataFrames for reference
    attrs = {
        'ytm_values': ytm_values,
        'dtm_values': dtm_values
    }

    raw_params_matrix.attrs.update(attrs)
    jw_params_matrix.attrs.update(attrs)

    return raw_params_matrix, jw_params_matrix


@catch_exception
def fit_model(market_data: pd.DataFrame,
              model_name: str = 'svi',
              initial_params: Optional[List[float]] = None,
              param_bounds: Optional[Tuple] = None) -> Dict[str, Any]:
    """
    Fit a volatility model to market data.

    Parameters:
    - market_data: DataFrame with market data
    - model_name: Type of model to fit (default: 'svi')
    - initial_params: Optional initial parameters for optimization (default: model's defaults)
    - param_bounds: Optional parameter bounds for optimization (default: model's defaults)

    Returns:
    - Dictionary with fitting results
    """
    if model_name.lower() != 'svi':
        raise VolyError(f"Model type '{model_name}' is not supported. Currently only 'svi' is available.")

    # Step 1: Fit model parameters and get performance metrics in one step
    fit_performance, params_dict = fit_svi_parameters(
        market_data,
        initial_params=initial_params,
        param_bounds=param_bounds
    )

    # Step 2: Create parameter matrices
    raw_params_matrix, jw_params_matrix = create_parameters_matrix(params_dict)

    return {
        'raw_params_matrix': raw_params_matrix,
        'jw_params_matrix': jw_params_matrix,
        'fit_performance': fit_performance,
    }


@catch_exception
def get_iv_surface(fit_results: Dict[str, Any],
                   log_moneyness_params: Tuple[float, float, int] = (-2, 2, 500)
                   ) -> Dict[str, Any]:
    """
    Generate implied volatility surface using optimized SVI parameters.

    Parameters:
    - fit_results: results from fit_model()
    - log_moneyness_params: Tuple of (min, max, num_points) for the moneyness grid

    Returns:
    - x_domain, iv_surface
    """
    iv_surface = {}

    # Extract moneyness parameters
    min_m, max_m, num_points = log_moneyness_params

    # Generate moneyness array
    log_moneyness_array = np.linspace(min_m, max_m, num=num_points)

    # Get YTM values from the parameter matrix attributes
    ytm_values = fit_results['fit_performance']['ytm']
    maturity_values = fit_results['fit_performance']['maturity_name']
    raw_params_matrix = fit_results['raw_params_matrix']

    # Generate implied volatility for each maturity
    for maturity, ytm in zip(maturity_values, ytm_values):
        svi_params = raw_params_matrix[maturity].values
        w_svi = [SVIModel.svi(x, *svi_params) for x in log_moneyness_array]
        iv_surface[maturity] = np.sqrt(np.array(w_svi) / ytm)

    return moneyness_array, iv_surface
