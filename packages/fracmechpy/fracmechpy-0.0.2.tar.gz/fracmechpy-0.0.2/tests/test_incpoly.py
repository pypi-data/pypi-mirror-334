# tests/test_incpoly.py

import unittest
import numpy as np  # type: ignore

from fracmechpy import IncPoly  # This will import the IncPoly function


class TestIncPolyFunction(unittest.TestCase):
    def test_incpoly_basic(self):
        # Sample data for testing (adjusted to use polynomial regression for af and ab)

        N = np.array([70000, 90000, 100000, 110000,120000,130000])
af = 
ab = np.array
        N = np.array([70000, 90000, 100000, 110000,120000,130000])
        af = np.array([1.90, 3.09, 3.78, 4.45, 6.19, 6.84])
        ab = np.array([0.89, 2.07, 2.81, 3.53, 5.09, 6.21])

        W = 50  # Width in (mm)
        p_max = 4000  # Maximum load in (N)
        p_min = 400  # Minimum load in (N)
        B = 5  # Thickness in (mm)
        n = 1  # Number of neighboring points for regression

        # Compute crack growth rate and stress intensity factor range using IncPoly method
        dadN_incpoly, dK_incpoly = IncPoly(N, af, ab, W, p_max, p_min, B, n)

        # Ensure that values are not None
        self.assertIsNotNone(dadN_incpoly)
        self.assertIsNotNone(dK_incpoly)

        # Ensure that the lengths of results are one less than the length of N
        self.assertEqual(len(dadN_incpoly), len(N) - 1)
        self.assertEqual(len(dK_incpoly), len(N) - 1)


unittest.main(argv=['first-arg-is-ignored'], exit=False)
