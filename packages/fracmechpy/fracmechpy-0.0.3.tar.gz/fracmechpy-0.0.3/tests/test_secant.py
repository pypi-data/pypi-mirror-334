# tests/test_secant.py

import unittest

import numpy as np  # type: ignore

from fracmechpy import Secant  # This will import the Secant function


class TestSecantFunction(unittest.TestCase):
    def test_secant_basic(self):
        N = np.array([560000, 570000, 580000, 590000])
        af = np.array([0.68, 5.04, 7.46, 10.86])
        ab = np.array([0.52, 5.02, 7.35, 10.21])
        W = 50  # Width in (mm)
        p_max = 4000  # Maximum load in (N)
        p_min = 400  # Minimum load in (N)
        B = 5  # Thickness in (m

        dadN, dK = Secant(N, af, ab, W, p_max, p_min, B)

        self.assertIsNotNone(dadN)
        self.assertIsNotNone(dK)
        self.assertEqual(len(dadN), len(N) - 1)
        self.assertEqual(len(dK), len(N) - 1)


unittest.main(argv=['first-arg-is-ignored'], exit=False)
