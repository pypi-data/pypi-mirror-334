"""
This module handles calculating risk-neutral densities from
fitted volatility models and converting to probability functions.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional, Union, Any
from voly.utils.logger import logger, catch_exception
from voly.exceptions import VolyError
from voly.models import SVIModel


@catch_exception
def rnd(moneyness_array: float, total_var: float) -> float:
    return np.exp(-(moneyness_array ** 2) / (2 * total_var)) / (np.sqrt(2 * np.pi * total_var))


@catch_exception
def get_rnd_surface(fit_results: Dict[str, Any],
                    moneyness_params: Tuple[float, float, int] = (-2, 2, 500)
                    ) -> Dict[str, Any]:
    """
    Calculate RND for all expiries using the SVI parameter matrix.

    Parameters:
    - moneyness_params: Tuple of (min, max, num_points) for the moneyness grid
    - fit_results: results from fit_model()

    Returns:
    - moneyness_array, rnd_surface
    """
    rnd_surface = {}

    # Extract moneyness parameters
    min_m, max_m, num_points = moneyness_params

    # Generate moneyness grid
    moneyness_array = np.linspace(min_m, max_m, num=num_points)

    # Get YTE values from the fit results attributes
    yte_values = fit_results['fit_performance']['YTE']
    maturity_values = fit_results['fit_performance']['Maturity']
    param_matrix = fit_results['raw_param_matrix']

    # Generate rnd for each expiry
    for maturity, yte in zip(maturity_values, yte_values):
        svi_params_list = list(param_matrix[maturity].values)
        a, b, sigma, rho, m = svi_params_list

        # Calculate total variance
        total_var = np.array([SVIModel.svi(x, a, b, sigma, rho, m) for x in moneyness_array])

        # Calculate risk-neutral density using the base RND function
        rnd_values = np.array([rnd(x, var) for x, var in zip(moneyness_array, total_var)])
        rnd_surface[maturity] = rnd_values

    return moneyness_array, rnd_surface


@catch_exception
def calculate_probability_thresholds(
        moneyness_grid: np.ndarray,
        rnd_values: np.ndarray,
        thresholds=None
) -> Dict[str, float]:
    """
    Calculate probabilities at specific log-moneyness thresholds.

    Parameters:
    - moneyness_grid: Grid of log-moneyness values
    - rnd_values: Risk-neutral density values
    - thresholds: Log-moneyness thresholds to calculate probabilities for

    Returns:
    - Dictionary mapping thresholds to their probabilities
    """
    # Calculate step size for integration
    if thresholds is None:
        thresholds = [-2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0]

    dx = moneyness_grid[1] - moneyness_grid[0]

    # Normalize the RND for proper probability
    total_density = np.sum(rnd_values) * dx
    normalized_rnd = rnd_values / total_density if total_density > 0 else rnd_values

    # Calculate cumulative distribution function (CDF)
    cdf = np.cumsum(normalized_rnd) * dx

    # Initialize probability results dictionary
    result = {}

    # Calculate probabilities for each threshold
    for threshold in thresholds:
        # Find the nearest index
        idx = np.abs(moneyness_grid - threshold).argmin()

        # Get exact threshold value (may be slightly different from requested)
        actual_threshold = moneyness_grid[idx]

        # Calculate probability P(X ≤ threshold)
        if idx < len(cdf):
            prob = cdf[idx]
        else:
            prob = 1.0

        # Calculate probability of exceeding positive thresholds
        # and probability of going below negative thresholds
        if threshold >= 0:
            # P(X > threshold) = 1 - P(X ≤ threshold)
            result[f"p_above_{threshold}"] = 1.0 - prob
        else:
            # P(X < threshold) = P(X ≤ threshold)
            result[f"p_below_{threshold}"] = prob

    return result


@catch_exception
def calculate_moments(
        moneyness_grid: np.ndarray,
        rnd_values: np.ndarray) -> Dict[str, float]:
    """
    Calculate statistical moments (mean, variance, skewness, kurtosis) of the RND.

    Parameters:
    - moneyness_grid: Grid of log-moneyness values
    - rnd_values: Array of RND values

    Returns:
    - Dictionary with statistical moments
    """
    # Calculate total probability (for normalization)
    dx = moneyness_grid[1] - moneyness_grid[0]
    total_prob = np.sum(rnd_values) * dx

    # Normalize the RND if needed
    normalized_rnd = rnd_values / total_prob if total_prob > 0 else rnd_values

    # Calculate moments in percentage terms
    # First, convert log-moneyness to percentage returns
    returns_pct = (np.exp(moneyness_grid) - 1) * 100  # Convert to percentage returns

    # Calculate mean (expected return in %)
    mean_pct = np.sum(returns_pct * normalized_rnd) * dx

    # Calculate variance (in % squared)
    centered_returns = returns_pct - mean_pct
    variance_pct = np.sum(centered_returns ** 2 * normalized_rnd) * dx
    std_dev_pct = np.sqrt(variance_pct)

    # Skewness and kurtosis are unitless
    skewness = np.sum(centered_returns ** 3 * normalized_rnd) * dx / (std_dev_pct ** 3) if std_dev_pct > 0 else 0
    kurtosis = np.sum(centered_returns ** 4 * normalized_rnd) * dx / (variance_pct ** 2) if variance_pct > 0 else 0

    return {
        "mean_pct": mean_pct,  # Mean return in percentage
        "variance_pct": variance_pct,  # Variance in percentage squared
        "std_dev_pct": std_dev_pct,  # Standard deviation in percentage
        "skewness": skewness,  # Unitless
        "kurtosis": kurtosis,  # Unitless
        "excess_kurtosis": kurtosis - 3  # Unitless
    }


@catch_exception
def analyze_rnd_statistics(
        moneyness_grid: np.ndarray,
        rnd_surface: Dict[str, np.ndarray],
        param_matrix: pd.DataFrame) -> pd.DataFrame:
    """
    Analyze RND statistics for all expiries.

    Parameters:
    - moneyness_grid: Grid of log-moneyness values
    - rnd_surface: Dictionary mapping maturity names to RND arrays
    - param_matrix: Matrix containing model parameters

    Returns:
    - DataFrame with RND statistics for each expiry
    """
    # Get maturity information
    dte_values = param_matrix.attrs['dte_values']
    yte_values = param_matrix.attrs['yte_values']

    # Initialize data dictionary
    data = {
        "maturity_name": [],
        "dte": [],
        "yte": [],
        "mean_pct": [],
        "std_dev_pct": [],
        "skewness": [],
        "excess_kurtosis": []
    }

    # Calculate moments for each expiry
    for maturity_name, rnd in rnd_surface.items():
        moments = calculate_moments(moneyness_grid, rnd)

        data["maturity_name"].append(maturity_name)
        data["dte"].append(dte_values[maturity_name])
        data["yte"].append(yte_values[maturity_name])
        data["mean_pct"].append(moments["mean_pct"])
        data["std_dev_pct"].append(moments["std_dev_pct"])
        data["skewness"].append(moments["skewness"])
        data["excess_kurtosis"].append(moments["excess_kurtosis"])

    # Create DataFrame and sort by DTE
    stats_df = pd.DataFrame(data)
    stats_df = stats_df.sort_values(by="dte")

    return stats_df


@catch_exception
def calculate_pdf(
        moneyness_grid: np.ndarray,
        rnd_values: np.ndarray,
        spot_price: float = 1.0
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Calculate probability density function (PDF) from RND values.

    Parameters:
    - moneyness_grid: Grid of log-moneyness values
    - rnd_values: Array of RND values
    - spot_price: Spot price of the underlying

    Returns:
    - Tuple of (prices, pdf_values) for plotting
    """
    # Calculate step size for normalization
    dx = moneyness_grid[1] - moneyness_grid[0]

    # Normalize the RND
    total_density = np.sum(rnd_values) * dx
    pdf_values = rnd_values / total_density if total_density > 0 else rnd_values

    # Convert log-moneyness to actual prices
    prices = spot_price * np.exp(moneyness_grid)

    return prices, pdf_values


@catch_exception
def calculate_cdf(
        moneyness_grid: np.ndarray,
        rnd_values: np.ndarray,
        spot_price: float = 1.0
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Calculate cumulative distribution function (CDF) from RND values.

    Parameters:
    - moneyness_grid: Grid of log-moneyness values
    - rnd_values: Array of RND values
    - spot_price: Spot price of the underlying

    Returns:
    - Tuple of (prices, cdf_values) for plotting
    """
    # Calculate step size for normalization
    dx = moneyness_grid[1] - moneyness_grid[0]

    # Normalize the RND
    total_density = np.sum(rnd_values) * dx
    normalized_rnd = rnd_values / total_density if total_density > 0 else rnd_values

    # Calculate CDF
    cdf_values = np.cumsum(normalized_rnd) * dx

    # Convert log-moneyness to actual prices
    prices = spot_price * np.exp(moneyness_grid)

    return prices, cdf_values


@catch_exception
def calculate_strike_probability(
        target_price: float,
        moneyness_grid: np.ndarray,
        rnd_values: np.ndarray,
        spot_price: float,
        direction: str = 'above'
) -> float:
    """
    Calculate probability of price being above or below a target price.

    Parameters:
    - target_price: Target price level
    - moneyness_grid: Grid of log-moneyness values
    - rnd_values: Array of RND values
    - spot_price: Current spot price
    - direction: 'above' or 'below'

    Returns:
    - Probability (0 to 1)
    """
    # Convert target price to log-moneyness
    target_moneyness = np.log(target_price / spot_price)

    # Calculate CDF
    _, cdf_values = calculate_cdf(moneyness_grid, rnd_values, spot_price)

    # Find the nearest index to target moneyness
    target_idx = np.abs(moneyness_grid - target_moneyness).argmin()

    # Get probability
    if target_idx < len(cdf_values):
        cdf_at_target = cdf_values[target_idx]
    else:
        cdf_at_target = 1.0

    # Return probability based on direction
    if direction.lower() == 'above':
        return 1.0 - cdf_at_target
    else:  # below
        return cdf_at_target


@catch_exception
def calculate_rnd(
        fit_results: Dict[str, Any],
        maturity: Optional[str] = None) -> Dict[str, Any]:
    """
    Calculate risk-neutral density from fit results.

    Parameters:
    - fit_results: Dictionary with fitting results from fit_model()
    - maturity: Optional maturity name to calculate RND for a specific expiry

    Returns:
    - Dictionary with RND results
    """
    # Extract required data from fit results
    raw_param_matrix = fit_results['raw_param_matrix']
    moneyness_grid = fit_results['moneyness_grid']

    # Calculate RND for all expiries or just the specified one
    if maturity is not None:
        # Validate maturity
        if maturity not in raw_param_matrix.columns:
            raise VolyError(f"Maturity '{maturity}' not found in fit results")

        # Just calculate for the specified maturity
        yte = raw_param_matrix.attrs['yte_values'][maturity]
        params = raw_param_matrix[maturity].values
        rnd_values = calculate_risk_neutral_density(moneyness_grid, params, yte)
        rnd_surface = {maturity: rnd_values}
    else:
        # Calculate for all maturities
        rnd_surface = calculate_rnd_for_all_expiries(moneyness_grid, raw_param_matrix)

    # Calculate statistics
    rnd_statistics = analyze_rnd_statistics(moneyness_grid, rnd_surface, raw_param_matrix)

    # Calculate probabilities
    rnd_probabilities = analyze_rnd_probabilities(moneyness_grid, rnd_surface, raw_param_matrix)

    return {
        'moneyness_grid': moneyness_grid,
        'rnd_surface': rnd_surface,
        'rnd_statistics': rnd_statistics,
        'rnd_probabilities': rnd_probabilities
    }
