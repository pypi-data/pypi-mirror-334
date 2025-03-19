"""
Main client interface for the Voly package.

This module provides the VolyClient class, which serves as the main
entry point for users to interact with the package functionality.
"""

import asyncio
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional, Union, Any, Callable
import plotly.graph_objects as go

from voly.utils.logger import logger, catch_exception, setup_file_logging
from voly.exceptions import VolyError
from voly.models import SVIModel
from voly.formulas import (
    d1, d2, bs, delta, gamma, vega, theta, rho, vanna, volga, charm, greeks, iv
)
from voly.core.data import fetch_option_chain, process_option_chain
from voly.core.fit import fit_model, get_iv_surface
from voly.core.rnd import get_rnd_surface, calculate_pdf, calculate_cdf, calculate_strike_probability
from voly.core.interpolate import interpolate_model
from voly.core.charts import (
    plot_all_smiles, plot_3d_surface, plot_parameters, plot_fit_performance,
    plot_fit_performance, plot_rnd, plot_pdf, plot_cdf, plot_rnd_all_expiries,
    plot_rnd_3d, plot_rnd_statistics, plot_interpolated_surface
)


class VolyClient:
    def __init__(self, enable_file_logging: bool = False, logs_dir: str = "logs/"):
        """
        Initialize the Voly client.

        Parameters:
        - enable_file_logging: Whether to enable file-based logging
        - logs_dir: Directory for log files if file logging is enabled
        """
        if enable_file_logging:
            setup_file_logging(logs_dir)

        logger.info("VolyClient initialized")
        self._loop = None  # For async operations

    def _get_event_loop(self):
        """Get or create an event loop for async operations"""
        try:
            self._loop = asyncio.get_event_loop()
        except RuntimeError:
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)
        return self._loop

    # -------------------------------------------------------------------------
    # Data Fetching and Processing
    # -------------------------------------------------------------------------

    def get_option_chain(self, exchange: str = 'deribit',
                         currency: str = 'BTC',
                         depth: bool = False) -> pd.DataFrame:
        """
        Fetch option chain data from the specified exchange.

        Parameters:
        - exchange: Exchange to fetch data from (currently only 'deribit' is supported)
        - currency: Currency to fetch options for (e.g., 'BTC', 'ETH')
        - depth: Whether to include full order book depth

        Returns:
        - Processed option chain data as a pandas DataFrame
        """
        logger.info(f"Fetching option chain data from {exchange} for {currency}")

        loop = self._get_event_loop()

        try:
            option_chain = loop.run_until_complete(
                fetch_option_chain(exchange, currency, depth)
            )
            return option_chain
        except VolyError as e:
            logger.error(f"Error fetching option chain: {str(e)}")
            raise

    # -------------------------------------------------------------------------
    # SVI, Black-Scholes and Greeks Calculations
    # -------------------------------------------------------------------------

    @staticmethod
    def svi(log_moneyness_array: float, a: float, b: float, sigma: float, rho: float, m: float) -> float:
        return SVIModel.svi(log_moneyness_array, a, b, sigma, rho, m)

    @staticmethod
    def svi_d(log_moneyness_array: float, a: float, b: float, sigma: float, rho: float, m: float) -> float:
        return SVIModel.svi_d(log_moneyness_array, a, b, sigma, rho, m)

    @staticmethod
    def svi_dd(log_moneyness_array: float, a: float, b: float, sigma: float, rho: float, m: float) -> float:
        return SVIModel.svi_dd(log_moneyness_array, a, b, sigma, rho, m)

    @staticmethod
    def d1(s: float, k: float, r: float, vol: float, t: float,
           option_type: str = 'call') -> float:
        return d1(s, k, r, vol, t, option_type)

    @staticmethod
    def d2(s: float, k: float, r: float, vol: float, t: float,
           option_type: str = 'call') -> float:
        return d2(s, k, r, vol, t, option_type)

    @staticmethod
    def bs(s: float, k: float, r: float, vol: float, t: float,
           option_type: str = 'call') -> float:
        """
        Calculate Black-Scholes option price.

        Parameters:
        - s: Underlying price
        - k: Strike price
        - r: Risk-free rate
        - vol: Volatility
        - t: Time to expiry in years
        - option_type: 'call' or 'put'

        Returns:
        - Option price
        """
        return bs(s, k, r, vol, t, option_type)

    @staticmethod
    def delta(s: float, k: float, r: float, vol: float, t: float,
              option_type: str = 'call') -> float:
        """
        Calculate option delta.

        Parameters:
        - s: Underlying price
        - k: Strike price
        - r: Risk-free rate
        - vol: Volatility
        - t: Time to expiry in years
        - option_type: 'call' or 'put'

        Returns:
        - Delta value
        """
        return delta(s, k, r, vol, t, option_type)

    @staticmethod
    def gamma(s: float, k: float, r: float, vol: float, t: float,
              option_type: str = 'call') -> float:
        """
        Calculate option gamma.

        Parameters:
        - s: Underlying price
        - k: Strike price
        - r: Risk-free rate
        - vol: Volatility
        - t: Time to expiry in years

        Returns:
        - Gamma value
        """
        return gamma(s, k, r, vol, t, option_type)

    @staticmethod
    def vega(s: float, k: float, r: float, vol: float, t: float,
             option_type: str = 'call') -> float:
        """
        Calculate option vega.

        Parameters:
        - s: Underlying price
        - k: Strike price
        - r: Risk-free rate
        - vol: Volatility
        - t: Time to expiry in years

        Returns:
        - Vega value (for 1% change in volatility)
        """
        return vega(s, k, r, vol, t, option_type)

    @staticmethod
    def theta(s: float, k: float, r: float, vol: float, t: float,
              option_type: str = 'call') -> float:
        """
        Calculate option theta.

        Parameters:
        - s: Underlying price
        - k: Strike price
        - r: Risk-free rate
        - vol: Volatility
        - t: Time to expiry in years
        - option_type: 'call' or 'put'

        Returns:
        - Theta value (per day)
        """
        return theta(s, k, r, vol, t, option_type)

    @staticmethod
    def rho(s: float, k: float, r: float, vol: float, t: float,
            option_type: str = 'call') -> float:
        """
        Calculate option rho.

        Parameters:
        - s: Underlying price
        - k: Strike price
        - r: Risk-free rate
        - vol: Volatility
        - t: Time to expiry in years
        - option_type: 'call' or 'put'

        Returns:
        - Rho value (for 1% change in interest rate)
        """
        return rho(s, k, r, vol, t, option_type)

    @staticmethod
    def vanna(s: float, k: float, r: float, vol: float, t: float,
              option_type: str = 'call') -> float:
        """
        Calculate option vanna.

        Parameters:
        - s: Underlying price
        - k: Strike price
        - r: Risk-free rate
        - vol: Volatility
        - t: Time to expiry in years

        Returns:
        - Vanna value
        """
        return vanna(s, k, r, vol, t, option_type)

    @staticmethod
    def volga(s: float, k: float, r: float, vol: float, t: float,
              option_type: str = 'call') -> float:
        """
        Calculate option volga (vomma).

        Parameters:
        - s: Underlying price
        - k: Strike price
        - r: Risk-free rate
        - vol: Volatility
        - t: Time to expiry in years

        Returns:
        - Volga value
        """
        return volga(s, k, r, vol, t, option_type)

    @staticmethod
    def charm(s: float, k: float, r: float, vol: float, t: float,
              option_type: str = 'call') -> float:
        """
        Calculate option charm (delta decay).

        Parameters:
        - s: Underlying price
        - k: Strike price
        - r: Risk-free rate
        - vol: Volatility
        - t: Time to expiry in years
        - option_type: 'call' or 'put'

        Returns:
        - Charm value (per day)
        """
        return charm(s, k, r, vol, t, option_type)

    @staticmethod
    def greeks(s: float, k: float, r: float, vol: float, t: float,
               option_type: str = 'call') -> Dict[str, float]:
        """
        Calculate all option Greeks.

        Parameters:
        - s: Underlying price
        - k: Strike price
        - r: Risk-free rate
        - vol: Volatility
        - t: Time to expiry in years
        - option_type: 'call' or 'put'

        Returns:
        - Dictionary with all Greeks (price, delta, gamma, vega, theta, rho, vanna, volga, charm)
        """
        return greeks(s, k, r, vol, t, option_type)

    @staticmethod
    def iv(option_price: float, s: float, k: float, r: float, t: float,
           option_type: str = 'call') -> float:
        """
        Calculate implied volatility.

        Parameters:
        - option_price: Market price of the option
        - s: Underlying price
        - k: Strike price
        - r: Risk-free rate
        - t: Time to expiry in years
        - option_type: 'call' or 'put'

        Returns:
        - Implied volatility
        """
        return iv(option_price, s, k, r, t, option_type)

    # -------------------------------------------------------------------------
    # Model Fitting
    # -------------------------------------------------------------------------

    @staticmethod
    def fit_model(market_data: pd.DataFrame,
                  model_name: str = 'svi',
                  initial_params: Optional[List[float]] = None,
                  param_bounds: Optional[Tuple] = None) -> Dict[str, Any]:
        """
        Fit a volatility model to market data.

        Parameters:
        - market_data: DataFrame with market data
        - model_name: Name of model to fit (default: 'svi')
        - initial_params: Optional initial parameters for optimization
        - param_bounds: Optional parameter bounds for optimization

        Returns:
        - Dictionary with fitting results and optional plots
        """
        logger.info(f"Fitting {model_name.upper()} model to market data")

        # Fit the model
        fit_results = fit_model(
            market_data=market_data,
            model_name=model_name,
            initial_params=initial_params,
            param_bounds=param_bounds
        )

        return fit_results

    @staticmethod
    def get_iv_surface(fit_results: Dict[str, Any],
                       moneyness_params: Tuple[float, float, int] = (-2, 2, 500)
                       ) -> Dict[str, Any]:
        """
        Generate implied volatility surface using optimized SVI parameters.

        Parameters:
        - param_matrix: Matrix of optimized SVI parameters from fit_results
        - moneyness_params: Tuple of (min, max, num_points) for the moneyness grid

        Returns:
        - Tuple of (moneyness_array, iv_surface)
        """
        # Generate the surface
        moneyness_array, iv_surface = get_iv_surface(
            fit_results=fit_results,
            moneyness_params=moneyness_params
        )

        return {
            'moneyness_array': moneyness_array,
            'iv_surface': iv_surface
        }

    @staticmethod
    def plot_model(fit_results: Dict[str, Any],
                   market_data: pd.DataFrame = None,
                   moneyness_params: Tuple[float, float, int] = (-2, 2, 500)
                   ) -> Dict[str, go.Figure]:
        """
        Generate all plots for the fitted model and RND results.

        Parameters:
        - fit_results: Dictionary with fitting results from fit_model()
        - market_data: Optional market data for comparison
        - moneyness_params: Grid of log-moneyness values

        Returns:
        - Dictionary of plot figures
        """
        plots = {}

        moneyness_array, iv_surface = get_iv_surface(fit_results, moneyness_params)

        # Extract data from fit results
        raw_param_matrix = fit_results['raw_param_matrix']
        jw_param_matrix = fit_results['jw_param_matrix']
        fit_performance = fit_results['fit_performance']

        # Plot volatility smiles
        plots['smiles'] = plot_all_smiles(moneyness_array, iv_surface, market_data)

        # Plot 3D surface
        plots['surface_3d'] = plot_3d_surface(moneyness_array, iv_surface)

        # Plot parameters
        plots['raw_params'], plots['jw_params'] = plot_parameters(raw_param_matrix, jw_param_matrix)

        # Plot fit statistics if available
        plots['fit_performance'] = plot_fit_performance(fit_performance)

        return plots

    # -------------------------------------------------------------------------
    # Risk-Neutral Density (RND)
    # -------------------------------------------------------------------------

    @staticmethod
    def get_rnd_surface(fit_results: Dict[str, Any],
                        moneyness_params: Tuple[float, float, int] = (-2, 2, 500)
                        ) -> Dict[str, np.ndarray]:
        """
        Calculate risk-neutral density from fitted model.

        Parameters:

        Returns:
        - Array with RND results over moneyness
        """
        logger.info("Calculating risk-neutral density")

        # Generate the surface
        moneyness_array, rnd_surface = get_rnd_surface(
            fit_results=fit_results,
            moneyness_params=moneyness_params
        )

        return {
            'moneyness_array': moneyness_array,
            'rnd_surface': rnd_surface
        }

    @staticmethod
    def pdf(rnd_results: Dict[str, Any],
            maturity: Optional[str] = None,
            plot: bool = False) -> Tuple[np.ndarray, np.ndarray]:
        """
        Calculate probability density function (PDF) from RND results.

        Parameters:
        - rnd_results: Dictionary with RND results from rnd()
        - maturity: Optional maturity name for a specific expiry
        - plot: Whether to generate and return a plot

        Returns:
        - Tuple of (prices, pdf_values) and optional plot
        """
        logger.info("Calculating PDF from RND")

        # Extract required data
        moneyness_grid = rnd_results['moneyness_grid']
        rnd_surface = rnd_results['rnd_surface']
        spot_price = rnd_results['spot_price']

        # Select maturity
        if maturity is None:
            # Use first maturity if not specified
            maturity = list(rnd_surface.keys())[0]
        elif maturity not in rnd_surface:
            raise VolyError(f"Maturity '{maturity}' not found in RND results")

        # Get RND values for the selected maturity
        rnd_values = rnd_surface[maturity]

        # Calculate PDF
        prices, pdf_values = calculate_pdf(moneyness_grid, rnd_values, spot_price)

        result = (prices, pdf_values)

        # Generate plot if requested
        if plot:
            logger.info(f"Generating PDF plot for {maturity}")
            pdf_plot = plot_pdf(
                moneyness_grid, rnd_values, spot_price,
                title=f"Probability Density Function - {maturity}"
            )
            result = (prices, pdf_values, pdf_plot)

        return result

    @staticmethod
    def cdf(rnd_results: Dict[str, Any],
            maturity: Optional[str] = None,
            plot: bool = False) -> Tuple[np.ndarray, np.ndarray]:
        """
        Calculate cumulative distribution function (CDF) from RND results.

        Parameters:
        - rnd_results: Dictionary with RND results from rnd()
        - maturity: Optional maturity name for a specific expiry
        - plot: Whether to generate and return a plot

        Returns:
        - Tuple of (prices, cdf_values) and optional plot
        """
        logger.info("Calculating CDF from RND")

        # Extract required data
        moneyness_grid = rnd_results['moneyness_grid']
        rnd_surface = rnd_results['rnd_surface']
        spot_price = rnd_results['spot_price']

        # Select maturity
        if maturity is None:
            # Use first maturity if not specified
            maturity = list(rnd_surface.keys())[0]
        elif maturity not in rnd_surface:
            raise VolyError(f"Maturity '{maturity}' not found in RND results")

        # Get RND values for the selected maturity
        rnd_values = rnd_surface[maturity]

        # Calculate CDF
        prices, cdf_values = calculate_cdf(moneyness_grid, rnd_values, spot_price)

        result = (prices, cdf_values)

        # Generate plot if requested
        if plot:
            logger.info(f"Generating CDF plot for {maturity}")
            cdf_plot = plot_cdf(
                moneyness_grid, rnd_values, spot_price,
                title=f"Cumulative Distribution Function - {maturity}"
            )
            result = (prices, cdf_values, cdf_plot)

        return result

    @staticmethod
    def probability(rnd_results: Dict[str, Any],
                    target_price: float,
                    maturity: Optional[str] = None,
                    direction: str = 'above') -> float:
        """
        Calculate the probability of price being above or below a target price.

        Parameters:
        - rnd_results: Dictionary with RND results from rnd()
        - target_price: Target price level
        - maturity: Optional maturity name for a specific expiry
        - direction: 'above' or 'below'

        Returns:
        - Probability (0 to 1)
        """
        if direction not in ['above', 'below']:
            raise VolyError("Direction must be 'above' or 'below'")

        # Extract required data
        moneyness_grid = rnd_results['moneyness_grid']
        rnd_surface = rnd_results['rnd_surface']
        spot_price = rnd_results['spot_price']

        # Select maturity
        if maturity is None:
            # Use first maturity if not specified
            maturity = list(rnd_surface.keys())[0]
        elif maturity not in rnd_surface:
            raise VolyError(f"Maturity '{maturity}' not found in RND results")

        # Get RND values for the selected maturity
        rnd_values = rnd_surface[maturity]

        # Calculate probability
        prob = calculate_strike_probability(
            target_price, moneyness_grid, rnd_values, spot_price, direction
        )

        return prob

    # -------------------------------------------------------------------------
    # Interpolation
    # -------------------------------------------------------------------------

    @staticmethod
    def interpolate(fit_results: Dict[str, Any],
                    specific_days: Optional[List[int]] = None,
                    num_points: int = 10,
                    method: str = 'cubic',
                    plot: bool = False) -> Dict[str, Any]:
        """
        Interpolate a fitted model to specific days to expiry.

        Parameters:
        - fit_results: Dictionary with fitting results from fit_model()
        - specific_days: Optional list of specific days to include (e.g., [7, 30, 90, 180])
        - num_points: Number of points for regular grid if specific_days is None
        - method: Interpolation method ('linear', 'cubic', 'pchip', etc.)
        - plot: Whether to generate and return a plot

        Returns:
        - Dictionary with interpolation results and optional plot
        """
        logger.info(f"Interpolating model with {method} method")

        # Interpolate the model
        interp_results = interpolate_model(
            fit_results, specific_days, num_points, method
        )

        # Generate plot if requested
        if plot:
            logger.info("Generating interpolated surface plot")
            interp_plot = plot_interpolated_surface(interp_results)
            interp_results['plot'] = interp_plot

        return interp_results
