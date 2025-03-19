"""
Option pricing formulas and general calculations.
"""

import numpy as np
from scipy.stats import norm
from typing import Tuple, Dict, Union, List, Optional
from voly.utils.logger import catch_exception
from voly.models import SVIModel
from math import exp


@catch_exception
def vectorize_inputs(func):
    """
    Decorator to vectorize Black-Scholes functions to handle both scalar and array inputs.
    """
    def wrapper(s, k, r, vol, t, option_type='call'):
        # Check if inputs are scalar
        k_scalar = np.isscalar(k)
        vol_scalar = np.isscalar(vol)

        # If both inputs are scalar, use the original function directly
        if k_scalar and vol_scalar:
            return func(s, k, r, vol, t, option_type)

        # Use NumPy's vectorize to handle array inputs
        vectorized_func = np.vectorize(lambda k_val, vol_val:
                                       func(s, k_val, r, vol_val, t, option_type))

        # Call the vectorized function with the inputs
        return vectorized_func(k, vol)

    return wrapper


@catch_exception
@vectorize_inputs
def d1(s: float, k: float, r: float, vol: float, t: float, option_type: str = 'call') -> float:
    # option_type is ignored in this function but included for compatibility
    if vol <= 0 or t <= 0:
        return np.nan
    return (np.log(s / k) + (r + vol ** 2 / 2) * t) / (vol * np.sqrt(t))

@catch_exception
@vectorize_inputs
def d2(s: float, k: float, r: float, vol: float, t: float, option_type: str = 'call') -> float:
    # option_type is ignored in this function but included for compatibility
    if vol <= 0 or t <= 0:
        return np.nan
    return d1(s, k, r, vol, t, option_type) - vol * np.sqrt(t)


@catch_exception
@vectorize_inputs
def bs(s: float, k: float, r: float, vol: float, t: float, option_type: str = 'call') -> float:
    if vol <= 0 or t <= 0:
        # Intrinsic value at expiry
        if option_type.lower() in ["call", "c"]:
            return max(0, s - k)
        else:
            return max(0, k - s)

    d1_val = d1(s, k, r, vol, t)
    d2_val = d2(s, k, r, vol, t)

    if option_type.lower() in ["call", "c"]:
        return s * norm.cdf(d1_val) - k * np.exp(-r * t) * norm.cdf(d2_val)
    else:  # put
        return k * np.exp(-r * t) * norm.cdf(-d2_val) - s * norm.cdf(-d1_val)


@catch_exception
@vectorize_inputs
def delta(s: float, k: float, r: float, vol: float, t: float, option_type: str = 'call') -> float:
    if vol <= 0 or t <= 0:
        # At expiry, delta is either 0 or 1 for call, 0 or -1 for put
        if option_type.lower() in ["call", "c"]:
            return 1.0 if s > k else 0.0
        else:
            return -1.0 if s < k else 0.0

    d1_val = d1(s, k, r, vol, t)

    if option_type.lower() in ["call", "c"]:
        return norm.cdf(d1_val)
    else:  # put
        return norm.cdf(d1_val) - 1.0


@catch_exception
@vectorize_inputs
def gamma(s: float, k: float, r: float, vol: float, t: float, option_type: str = 'call') -> float:
    if vol <= 0 or t <= 0:
        return 0.0

    d1_val = d1(s, k, r, vol, t, option_type)
    return norm.pdf(d1_val) / (s * vol * np.sqrt(t))


@catch_exception
@vectorize_inputs
def vega(s: float, k: float, r: float, vol: float, t: float, option_type: str = 'call') -> float:
    if vol <= 0 or t <= 0:
        return 0.0

    d1_val = d1(s, k, r, vol, t, option_type)
    return s * norm.pdf(d1_val) * np.sqrt(t) / 100  # Divided by 100 for 1% change


@catch_exception
@vectorize_inputs
def theta(s: float, k: float, r: float, vol: float, t: float, option_type: str = 'call') -> float:
    if vol <= 0 or t <= 0:
        return 0.0

    d1_val = d1(s, k, r, vol, t, option_type)
    d2_val = d2(s, k, r, vol, t, option_type)

    # First part of theta (same for both call and put)
    theta_part1 = -s * norm.pdf(d1_val) * vol / (2 * np.sqrt(t))

    # Second part depends on option type
    if option_type.lower() in ["call", "c"]:
        theta_part2 = -r * k * np.exp(-r * t) * norm.cdf(d2_val)
    else:  # put
        theta_part2 = r * k * np.exp(-r * t) * norm.cdf(-d2_val)

    # Return theta per day (t is in years)
    return (theta_part1 + theta_part2) / 365.0


@catch_exception
@vectorize_inputs
def rho(s: float, k: float, r: float, vol: float, t: float, option_type: str = 'call') -> float:
    if vol <= 0 or t <= 0:
        return 0.0

    d2_val = d2(s, k, r, vol, t, option_type)

    if option_type.lower() in ["call", "c"]:
        return k * t * np.exp(-r * t) * norm.cdf(d2_val) / 100
    else:  # put
        return -k * t * np.exp(-r * t) * norm.cdf(-d2_val) / 100


@catch_exception
@vectorize_inputs
def vanna(s: float, k: float, r: float, vol: float, t: float, option_type: str = 'call') -> float:
    if vol <= 0 or t <= 0:
        return 0.0

    d1_val = d1(s, k, r, vol, t, option_type)
    d2_val = d2(s, k, r, vol, t, option_type)

    return -norm.pdf(d1_val) * d2_val / vol


@catch_exception
@vectorize_inputs
def volga(s: float, k: float, r: float, vol: float, t: float, option_type: str = 'call') -> float:
    if vol <= 0 or t <= 0:
        return 0.0

    d1_val = d1(s, k, r, vol, t, option_type)
    d2_val = d2(s, k, r, vol, t, option_type)

    return s * norm.pdf(d1_val) * np.sqrt(t) * d1_val * d2_val / vol


@catch_exception
@vectorize_inputs
def charm(s: float, k: float, r: float, vol: float, t: float, option_type: str = 'call') -> float:
    if vol <= 0 or t <= 0:
        return 0.0

    d1_val = d1(s, k, r, vol, t, option_type)
    d2_val = d2(s, k, r, vol, t, option_type)

    # First term is the same for calls and puts
    term1 = -norm.pdf(d1_val) * d1_val / (2 * t)

    # Second term depends on option type
    if option_type.lower() in ["call", "c"]:
        term2 = -r * np.exp(-r * t) * norm.cdf(d2_val)
    else:  # put
        term2 = r * np.exp(-r * t) * norm.cdf(-d2_val)

    # Return charm per day (t is in years)
    return (term1 + term2) / 365.25


@catch_exception
@vectorize_inputs
def greeks(s: float, k: float, r: float, vol: float, t: float,
           option_type: str = 'call') -> Dict[str, float]:
    return {
        'price': bs(s, k, r, vol, t, option_type),
        'delta': delta(s, k, r, vol, t, option_type),
        'gamma': gamma(s, k, r, vol, t, option_type),
        'vega': vega(s, k, r, vol, t, option_type),
        'theta': theta(s, k, r, vol, t, option_type),
        'rho': rho(s, k, r, vol, t, option_type),
        'vanna': vanna(s, k, r, vol, t, option_type),
        'volga': volga(s, k, r, vol, t, option_type),
        'charm': charm(s, k, r, vol, t, option_type)
    }


@catch_exception
@vectorize_inputs
def iv(option_price: float, s: float, k: float, r: float, t: float,
       option_type: str = 'call', precision: float = 1e-8,
       max_iterations: int = 100) -> float:
    """
    Calculate implied volatility using Newton-Raphson method.

    Parameters:
    - option_price: Market price of the option
    - s: Underlying price
    - k: Strike price
    - r: Risk-free rate
    - t: Time to expiry in years
    - option_type: 'call' or 'put'
    - precision: Desired precision
    - max_iterations: Maximum number of iterations

    Returns:
    - Implied volatility
    """
    if t <= 0:
        return np.nan

    # Check if option price is within theoretical bounds
    if option_type.lower() in ["call", "c"]:
        intrinsic = max(0, s - k * np.exp(-r * t))
        if option_price < intrinsic:
            return np.nan  # Price below intrinsic value
        if option_price >= s:
            return np.inf  # Price exceeds underlying
    else:  # put
        intrinsic = max(0, k * np.exp(-r * t) - s)
        if option_price < intrinsic:
            return np.nan  # Price below intrinsic value
        if option_price >= k:
            return np.inf  # Price exceeds strike

    # Initial guess - Manaster and Koehler (1982) method
    vol = np.sqrt(2 * np.pi / t) * option_price / s

    # Ensure initial guess is reasonable
    vol = max(0.001, min(vol, 5.0))

    for _ in range(max_iterations):
        # Calculate option price and vega with current volatility
        price = bs(s, k, r, vol, t, option_type)
        v = vega(s, k, r, vol, t)

        # Calculate price difference
        price_diff = price - option_price

        # Check if precision reached
        if abs(price_diff) < precision:
            return vol

        # Avoid division by zero
        if abs(v) < 1e-10:
            # Change direction based on whether price is too high or too low
            vol = vol * 1.5 if price_diff < 0 else vol * 0.5
        else:
            # Newton-Raphson update
            vol = vol - price_diff / (v * 100)  # Vega is for 1% change

        # Ensure volatility stays in reasonable bounds
        vol = max(0.001, min(vol, 5.0))

    # If we reach here, we didn't converge
    return np.nan
