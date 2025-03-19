"""
Surface interpolation module for the Voly package.

This module handles interpolation of implied volatility surfaces
across both moneyness and time dimensions.
"""

import numpy as np
import pandas as pd
from typing import List, Tuple, Dict, Optional, Union, Any
from scipy.interpolate import interp1d, pchip_interpolate
from voly.utils.logger import logger, catch_exception
from voly.exceptions import VolyError
from voly.models import SVIModel


@catch_exception
def interpolate_surface_time(
        moneyness_grid: np.ndarray,
        expiries: np.ndarray,
        surface_values: np.ndarray,
        target_expiries: np.ndarray,
        method: str = 'cubic'
) -> np.ndarray:
    """
    Interpolate the surface across the time dimension.

    Parameters:
    - moneyness_grid: Array of log-moneyness values
    - expiries: Array of expiry times (in years)
    - surface_values: 2D array of values to interpolate (rows=expiries, cols=moneyness)
    - target_expiries: Array of target expiry times to interpolate to
    - method: Interpolation method ('linear', 'cubic', 'pchip', etc.)

    Returns:
    - 2D array of interpolated values (rows=target_expiries, cols=moneyness)
    """
    if len(expiries) < 2:
        raise VolyError("At least two expiries are required for time interpolation")

    # Initialize the output array
    interpolated_surface = np.zeros((len(target_expiries), len(moneyness_grid)))

    # For each moneyness point, interpolate across time
    for i in range(len(moneyness_grid)):
        if method == 'pchip':
            # Use PCHIP (Piecewise Cubic Hermite Interpolating Polynomial)
            interpolated_values = pchip_interpolate(expiries, surface_values[:, i], target_expiries)
        else:
            # Use regular interpolation (linear, cubic, etc.)
            interp_func = interp1d(expiries, surface_values[:, i], kind=method, bounds_error=False,
                                   fill_value='extrapolate')
            interpolated_values = interp_func(target_expiries)

        interpolated_surface[:, i] = interpolated_values

    return interpolated_surface


@catch_exception
def create_target_expiries(
        min_dte: float,
        max_dte: float,
        num_points: int = 10,
        specific_days: Optional[List[int]] = None
) -> np.ndarray:
    """
    Create a grid of target expiry days for interpolation.

    Parameters:
    - min_dte: Minimum days to expiry
    - max_dte: Maximum days to expiry
    - num_points: Number of points for regular grid
    - specific_days: Optional list of specific days to include (e.g., [7, 30, 90, 180])

    Returns:
    - Array of target expiry times in years
    """
    # Create regular grid in days
    if specific_days is not None:
        # Filter specific days to be within range
        days = np.array([d for d in specific_days if min_dte <= d <= max_dte])
        if len(days) == 0:
            logger.warning("No specific days within range, using regular grid")
            days = np.linspace(min_dte, max_dte, num_points)
    else:
        # Use regular grid
        days = np.linspace(min_dte, max_dte, num_points)

    # Convert to years
    years = days / 365.25

    return years


@catch_exception
def interpolate_svi_parameters(
        raw_param_matrix: pd.DataFrame,
        target_expiries_years: np.ndarray,
        method: str = 'cubic'
) -> pd.DataFrame:
    """
    Interpolate SVI parameters across time.

    Parameters:
    - raw_param_matrix: Matrix of SVI parameters with maturity names as columns
    - target_expiries_years: Array of target expiry times (in years)
    - method: Interpolation method ('linear', 'cubic', 'pchip', etc.)

    Returns:
    - Matrix of interpolated SVI parameters
    """
    # Get expiry times in years from the parameter matrix
    yte_values = raw_param_matrix.attrs['yte_values']
    dte_values = raw_param_matrix.attrs['dte_values']

    # Sort maturity names by DTE
    maturity_names = sorted(yte_values.keys(), key=lambda x: dte_values[x])

    # Extract expiry times in order
    expiry_years = np.array([yte_values[m] for m in maturity_names])

    # Check if we have enough points for interpolation
    if len(expiry_years) < 2:
        raise VolyError("At least two expiries are required for interpolation")

    # Create new parameter matrix for interpolated values
    interp_param_matrix = pd.DataFrame(
        columns=[f"t{i:.2f}" for i in target_expiries_years],
        index=SVIModel.PARAM_NAMES
    )

    # For each SVI parameter, interpolate across time
    for param in SVIModel.PARAM_NAMES:
        param_values = np.array([raw_param_matrix.loc[param, m] for m in maturity_names])

        if method == 'pchip':
            interpolated_values = pchip_interpolate(expiry_years, param_values, target_expiries_years)
        else:
            interp_func = interp1d(expiry_years, param_values, kind=method, bounds_error=False,
                                   fill_value='extrapolate')
            interpolated_values = interp_func(target_expiries_years)

        # Store interpolated values
        for i, t in enumerate(target_expiries_years):
            interp_param_matrix.loc[param, f"t{t:.2f}"] = interpolated_values[i]

    # Create matching DTE values for convenience
    interp_dte_values = target_expiries_years * 365.25

    # Store YTE and DTE as attributes in the DataFrame for reference
    interp_param_matrix.attrs['yte_values'] = {f"t{t:.2f}": t for t in target_expiries_years}
    interp_param_matrix.attrs['dte_values'] = {f"t{t:.2f}": t * 365.25 for t in target_expiries_years}

    return interp_param_matrix


@catch_exception
def interpolate_model(
        fit_results: Dict[str, Any],
        specific_days: Optional[List[int]] = None,
        num_points: int = 10,
        method: str = 'cubic'
) -> Dict[str, Any]:
    """
    Interpolate a fitted model to specific days to expiry.

    Parameters:
    - fit_results: Dictionary with fitting results from fit_model()
    - specific_days: Optional list of specific days to include (e.g., [7, 30, 90, 180])
    - num_points: Number of points for regular grid if specific_days is None
    - method: Interpolation method ('linear', 'cubic', 'pchip', etc.)

    Returns:
    - Dictionary with interpolation results
    """
    # Extract required data from fit results
    raw_param_matrix = fit_results['raw_param_matrix']
    moneyness_grid = fit_results['moneyness_grid']

    # Get min and max DTE from the original data
    dte_values = list(raw_param_matrix.attrs['dte_values'].values())
    min_dte = min(dte_values)
    max_dte = max(dte_values)

    # Create target expiry grid
    target_expiries_years = create_target_expiries(min_dte, max_dte, num_points, specific_days)

    # Interpolate SVI parameters
    interp_param_matrix = interpolate_svi_parameters(raw_param_matrix, target_expiries_years, method)

    # Generate implied volatility surface from interpolated parameters
    iv_surface = {}
    for maturity_name, yte in interp_param_matrix.attrs['yte_values'].items():
        svi_params = interp_param_matrix[maturity_name].values
        w_svi = [SVIModel.svi(x, *svi_params) for x in moneyness_grid]
        iv_surface[yte] = np.sqrt(np.array(w_svi) / yte)

    # Convert to Jump-Wing parameters for the interpolated maturities
    jw_param_matrix = pd.DataFrame(
        columns=interp_param_matrix.columns,
        index=SVIModel.JW_PARAM_NAMES
    )

    for maturity_name, yte in interp_param_matrix.attrs['yte_values'].items():
        a, b, sigma, rho, m = interp_param_matrix[maturity_name].values
        nu, psi, p, c, nu_tilde = SVIModel.svi_jw_params(a, b, sigma, rho, m, yte)
        jw_param_matrix[maturity_name] = [nu, psi, p, c, nu_tilde]

    # Copy attributes from param matrix
    jw_param_matrix.attrs = interp_param_matrix.attrs.copy()

    return {
        'moneyness_grid': moneyness_grid,
        'target_expiries_years': target_expiries_years,
        'target_expiries_days': target_expiries_years * 365.25,
        'interp_param_matrix': interp_param_matrix,
        'interp_jw_param_matrix': jw_param_matrix,
        'iv_surface': iv_surface,
        'method': method
    }