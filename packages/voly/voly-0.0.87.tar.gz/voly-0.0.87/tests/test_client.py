"""
Comprehensive tests for the VolyClient class with detailed output.
This file demonstrates expected values and provides informative output.
"""

import unittest
import numpy as np
from voly import VolyClient
import sys


class VolyClientTestCase(unittest.TestCase):
    """
    Test cases for the VolyClient class with expected values and detailed output.
    """

    def setUp(self):
        """Set up test fixtures."""
        self.voly = VolyClient()
        # Add a divider line before each test for clearer output
        print("\n" + "=" * 80)

    def test_bs_pricing_with_expected_values(self):
        """Test Black-Scholes pricing with expected values."""
        print("\nTEST: Black-Scholes Pricing")

        # Test parameters
        s = 100.0
        k = 100.0
        r = 0.05
        vol = 0.2
        t = 1.0

        # Expected values (pre-calculated)
        expected_call = 10.45
        expected_put = 5.57

        # Calculate actual values
        actual_call = self.voly.bs(s=s, k=k, r=r, vol=vol, t=t, option_type='call')
        actual_put = self.voly.bs(s=s, k=k, r=r, vol=vol, t=t, option_type='put')

        # Print actual vs expected
        print(f"Parameters: S={s}, K={k}, r={r}, vol={vol}, t={t}")
        print(
            f"Call Price: Actual={actual_call:.4f}, Expected={expected_call:.4f}, Diff={abs(actual_call - expected_call):.6f}")
        print(
            f"Put Price: Actual={actual_put:.4f}, Expected={expected_put:.4f}, Diff={abs(actual_put - expected_put):.6f}")

        # Check put-call parity
        pcp_diff = actual_call - actual_put - s + k * np.exp(-r * t)
        print(f"Put-Call Parity Check: {pcp_diff:.8f} (should be close to 0)")

        # Assertions with tolerance
        self.assertAlmostEqual(actual_call, expected_call, delta=0.01,
                               msg=f"Call price {actual_call:.4f} doesn't match expected {expected_call:.4f}")
        self.assertAlmostEqual(actual_put, expected_put, delta=0.01,
                               msg=f"Put price {actual_put:.4f} doesn't match expected {expected_put:.4f}")
        self.assertAlmostEqual(pcp_diff, 0, delta=1e-10,
                               msg="Put-call parity violated")

    def test_delta_values_across_moneyness(self):
        """Test delta values across different moneyness levels."""
        print("\nTEST: Delta Values Across Moneyness")

        # Test parameters
        s = 100.0
        r = 0.05
        vol = 0.2
        t = 1.0

        # Define test cases: strike, expected call delta, expected put delta
        test_cases = [
            (50.0, 0.9999, -0.0001),  # Deep ITM call / Deep OTM put
            (75.0, 0.9631, -0.0369),  # ITM call / OTM put
            (100.0, 0.6368, -0.3632),  # ATM
            (125.0, 0.2219, -0.7781),  # OTM call / ITM put
            (150.0, 0.0467, -0.9533)  # Deep OTM call / Deep ITM put
        ]

        print(f"Parameters: S={s}, r={r}, vol={vol}, t={t}")
        print("\nDelta Values:")
        print(f"{'Strike':<10} {'Call Delta':<15} {'Expected':<15} {'Put Delta':<15} {'Expected':<15}")
        print("-" * 70)

        for strike, exp_call_delta, exp_put_delta in test_cases:
            call_delta = self.voly.delta(s=s, k=strike, r=r, vol=vol, t=t, option_type='call')
            put_delta = self.voly.delta(s=s, k=strike, r=r, vol=vol, t=t, option_type='put')

            print(f"{strike:<10.1f} {call_delta:<15.4f} {exp_call_delta:<15.4f} "
                  f"{put_delta:<15.4f} {exp_put_delta:<15.4f}")

            # Check deltas are within expected range
            self.assertAlmostEqual(call_delta, exp_call_delta, delta=0.01,
                                   msg=f"Call delta for K={strike} incorrect")
            self.assertAlmostEqual(put_delta, exp_put_delta, delta=0.01,
                                   msg=f"Put delta for K={strike} incorrect")

            # Check put-call delta relationship: call_delta - put_delta = 1
            self.assertAlmostEqual(call_delta - put_delta, 1.0, delta=1e-10,
                                   msg="Delta relationship violated")

    def test_all_greeks_values(self):
        """Test all Greeks calculation with expected values."""
        print("\nTEST: All Greeks Values")

        # Test parameters
        s = 100.0
        k = 100.0
        r = 0.05
        vol = 0.2
        t = 1.0

        # Calculate all Greeks for a call
        call_greeks = self.voly.greeks(s=s, k=k, r=r, vol=vol, t=t, option_type='call')

        # Expected values (calculated using standard Black-Scholes formulas)
        expected_greeks = {
            'price': 10.45,
            'delta': 0.637,
            'gamma': 0.019,
            'vega': 0.375,
            'theta': -0.018,
            'rho': 0.52,
        }

        print(f"Parameters: S={s}, K={k}, r={r}, vol={vol}, t={t}")
        print("\nCall Option Greeks:")
        print(f"{'Greek':<10} {'Actual':<15} {'Expected':<15} {'Diff':<15}")
        print("-" * 55)

        for greek, expected in expected_greeks.items():
            actual = call_greeks[greek]
            print(f"{greek.capitalize():<10} {actual:<15.6f} {expected:<15.6f} {abs(actual - expected):<15.6f}")

            # Assert with appropriate tolerance
            self.assertAlmostEqual(actual, expected, delta=max(0.01, expected * 0.05),
                                   msg=f"{greek.capitalize()} value incorrect")

        # Additional checks for other Greeks
        print("\nAdditional Greeks:")
        for greek in ['vanna', 'volga', 'charm']:
            if greek in call_greeks:
                print(f"{greek.capitalize():<10} {call_greeks[greek]:<15.6f}")

        # Check basic relationships
        # Gamma should be positive for both calls and puts
        self.assertGreater(call_greeks['gamma'], 0, "Gamma should be positive")

        # Vega should be positive for both calls and puts
        self.assertGreater(call_greeks['vega'], 0, "Vega should be positive")

        # Theta is typically negative for calls and puts (time decay)
        self.assertLess(call_greeks['theta'], 0, "Theta should be negative for calls")

    def test_implied_volatility_calculation(self):
        """Test implied volatility calculation with known prices."""
        print("\nTEST: Implied Volatility Calculation")

        # Define test cases
        test_cases = [
            # S, K, r, vol, t
            (100.0, 100.0, 0.05, 0.2, 1.0),  # ATM
            (100.0, 90.0, 0.05, 0.25, 0.5),  # ITM
            (100.0, 110.0, 0.05, 0.3, 0.25)  # OTM
        ]

        print(f"{'S':<8} {'K':<8} {'r':<8} {'t':<8} {'Input Vol':<12} {'Option Price':<15} "
              f"{'Implied Vol':<15} {'Diff':<10}")
        print("-" * 90)

        for s, k, r, vol, t in test_cases:
            # Calculate option price with known volatility
            call_price = self.voly.bs(s=s, k=k, r=r, vol=vol, t=t, option_type='call')

            # Calculate implied volatility from the price
            try:
                implied_vol = self.voly.iv(option_price=call_price, s=s, k=k, r=r, t=t, option_type='call')
                vol_diff = abs(vol - implied_vol)
                print(f"{s:<8.1f} {k:<8.1f} {r:<8.3f} {t:<8.2f} {vol:<12.4f} {call_price:<15.6f} "
                      f"{implied_vol:<15.6f} {vol_diff:<10.6f}")

                # Assert implied vol matches input vol
                self.assertAlmostEqual(vol, implied_vol, delta=0.0001,
                                       msg=f"Implied volatility {implied_vol:.6f} doesn't match input {vol:.6f}")
            except Exception as e:
                print(f"{s:<8.1f} {k:<8.1f} {r:<8.3f} {t:<8.2f} {vol:<12.4f} {call_price:<15.6f} "
                      f"ERROR: {str(e)}")
                self.fail(f"Implied volatility calculation failed: {str(e)}")

    def test_bs_pricing_extreme_cases(self):
        """Test Black-Scholes pricing under extreme conditions."""
        print("\nTEST: Black-Scholes Pricing - Extreme Cases")

        # Test zero volatility
        zero_vol_call = self.voly.bs(s=100, k=90, r=0.05, vol=0, t=1, option_type='call')
        zero_vol_put = self.voly.bs(s=100, k=110, r=0.05, vol=0, t=1, option_type='put')

        print("Zero Volatility:")
        print(f"Call (S=100, K=90): {zero_vol_call:.4f} (should equal intrinsic value 10)")
        print(f"Put (S=100, K=110): {zero_vol_put:.4f} (should equal intrinsic value 10)")

        self.assertAlmostEqual(zero_vol_call, 10.0, delta=0.01,
                               msg="Zero vol ITM call should equal intrinsic value")
        self.assertAlmostEqual(zero_vol_put, 10.0, delta=0.01,
                               msg="Zero vol ITM put should equal intrinsic value")

        # Test zero time to expiry
        zero_time_call = self.voly.bs(s=100, k=90, r=0.05, vol=0.2, t=0, option_type='call')
        zero_time_put = self.voly.bs(s=100, k=110, r=0.05, vol=0.2, t=0, option_type='put')

        print("\nZero Time to Expiry:")
        print(f"Call (S=100, K=90): {zero_time_call:.4f} (should equal intrinsic value 10)")
        print(f"Put (S=100, K=110): {zero_time_put:.4f} (should equal intrinsic value 10)")

        self.assertAlmostEqual(zero_time_call, 10.0, delta=0.01,
                               msg="Zero time ITM call should equal intrinsic value")
        self.assertAlmostEqual(zero_time_put, 10.0, delta=0.01,
                               msg="Zero time ITM put should equal intrinsic value")

        # Test deep ITM and OTM
        deep_itm_call = self.voly.bs(s=100, k=50, r=0.05, vol=0.2, t=1, option_type='call')
        deep_otm_call = self.voly.bs(s=100, k=200, r=0.05, vol=0.2, t=1, option_type='call')

        print("\nDeep ITM/OTM:")
        print(f"Deep ITM Call (S=100, K=50): {deep_itm_call:.4f}")
        print(f"Deep OTM Call (S=100, K=200): {deep_otm_call:.4f}")

        self.assertGreater(deep_itm_call, 50.0,
                           msg="Deep ITM call should be greater than intrinsic value")
        self.assertGreater(deep_otm_call, 0.0,
                           msg="Deep OTM call should have positive value")
        self.assertLess(deep_otm_call, 5.0,
                        msg="Deep OTM call should have small value")


if __name__ == '__main__':
    # More detailed output
    print("\nVOLY CLIENT DETAILED TEST SUITE")
    print("=" * 80)
    print(f"Testing against expected values for options pricing and Greeks")
    print("-" * 80)

    # Run tests with more verbose output
    unittest.main(verbosity=2)
