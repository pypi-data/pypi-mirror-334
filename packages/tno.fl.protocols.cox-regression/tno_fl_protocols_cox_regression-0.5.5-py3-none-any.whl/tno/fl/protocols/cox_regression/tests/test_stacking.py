"""
Test suite for testing the correctness of the stacking function.
"""

from __future__ import annotations

import unittest

import lifelines.datasets  # type: ignore
import numpy as np

from tno.fl.protocols.cox_regression.survival_stacking import stack, stack_time_varying


class TestSurvivalStacking(unittest.TestCase):
    """Test cases for survival stacking module"""

    def test_stack_static_lifelines(self) -> None:
        """
        Validates non-time varying stacking function, no time bins.
        Uses a small data set from lifelines.
        Tested against a manually stacked version.
        """
        data = lifelines.datasets.load_static_test()
        covariates = data[["var1", "var2"]].to_numpy()
        times = data["t"].to_numpy() + 1
        failed = data["E"].to_numpy()

        stacked, target = stack(
            covariates=covariates,
            times=times,
            events=failed,
        )

        combined = np.column_stack((stacked, target))
        correct_combined = np.array(
            [
                [-1.0, -1.0, 1.0, 0.0, 0.0, 0.0, 0.0],
                [-2.0, -2.0, 1.0, 0.0, 0.0, 0.0, 0.0],
                [-3.0, -3.0, 1.0, 0.0, 0.0, 0.0, 0.0],
                [-4.0, -4.0, 1.0, 0.0, 0.0, 0.0, 0.0],
                [-5.0, -5.0, 1.0, 0.0, 0.0, 0.0, 0.0],
                [-6.0, -6.0, 1.0, 0.0, 0.0, 0.0, 1.0],
                [-7.0, -7.0, 1.0, 0.0, 0.0, 0.0, 0.0],
                [-1.0, -1.0, 0.0, 1.0, 0.0, 0.0, 0.0],
                [-2.0, -2.0, 0.0, 1.0, 0.0, 0.0, 0.0],
                [-3.0, -3.0, 0.0, 1.0, 0.0, 0.0, 0.0],
                [-4.0, -4.0, 0.0, 1.0, 0.0, 0.0, 0.0],
                [-5.0, -5.0, 0.0, 1.0, 0.0, 0.0, 1.0],
                [-7.0, -7.0, 0.0, 1.0, 0.0, 0.0, 1.0],
                [-1.0, -1.0, 0.0, 0.0, 1.0, 0.0, 0.0],
                [-2.0, -2.0, 0.0, 0.0, 1.0, 0.0, 1.0],
                [-3.0, -3.0, 0.0, 0.0, 1.0, 0.0, 0.0],
                [-4.0, -4.0, 0.0, 0.0, 1.0, 0.0, 0.0],
                [-1.0, -1.0, 0.0, 0.0, 0.0, 1.0, 1.0],
                [-4.0, -4.0, 0.0, 0.0, 0.0, 1.0, 1.0],
            ]
        )

        np.testing.assert_array_equal(combined, correct_combined)

    def test_stack_static_lifelines_time_bins(self) -> None:
        """
        Validates non-time varying stacking function with time bins
        Uses a small data set from lifelines.
        Tested against a manually stacked version.
        """
        data = lifelines.datasets.load_static_test()
        covariates = data[["var1", "var2"]].to_numpy()
        times = data["t"].to_numpy() + 1
        failed = data["E"].to_numpy()
        time_bins = np.array([0, 3, 5, 7])

        stacked, target = stack(
            covariates=covariates, times=times, events=failed, time_bins=time_bins
        )

        combined = np.column_stack((stacked, target))
        correct_combined = np.array(
            [
                [-1.0, -1.0, 1.0, 0.0, 0.0, 0.0],
                [-2.0, -2.0, 1.0, 0.0, 0.0, 0.0],
                [-3.0, -3.0, 1.0, 0.0, 0.0, 0.0],
                [-4.0, -4.0, 1.0, 0.0, 0.0, 0.0],
                [-5.0, -5.0, 1.0, 0.0, 0.0, 0.0],
                [-6.0, -6.0, 1.0, 0.0, 0.0, 1.0],
                [-7.0, -7.0, 1.0, 0.0, 0.0, 0.0],
                [-1.0, -1.0, 0.0, 1.0, 0.0, 0.0],
                [-2.0, -2.0, 0.0, 1.0, 0.0, 1.0],
                [-3.0, -3.0, 0.0, 1.0, 0.0, 0.0],
                [-4.0, -4.0, 0.0, 1.0, 0.0, 0.0],
                [-5.0, -5.0, 0.0, 1.0, 0.0, 1.0],
                [-7.0, -7.0, 0.0, 1.0, 0.0, 1.0],
                [-1.0, -1.0, 0.0, 0.0, 1.0, 1.0],
                [-4.0, -4.0, 0.0, 0.0, 1.0, 1.0],
            ]
        )

        np.testing.assert_array_equal(combined, correct_combined)

    def test_stack_toy_example(self) -> None:
        """
        Validates the stack function using a handwritten toy example.
        The data and the solution have been created by hand.
        """

        covariates = np.array(
            [[0.1, 0.0], [0.5, 0.0], [0.5, 1.0], [0.7, 1.0]], dtype=float
        )
        ids = np.array([1, 2, 2, 3], dtype=int)
        start_times = np.array([0, 0, 3, 0], dtype=float)
        end_times = np.array([1, 3, 15, 4], dtype=float)
        failed = np.array([True, False, True, True], dtype=bool)

        stacked, target = stack_time_varying(
            ids, covariates, start_times, end_times, failed
        )

        combined = np.column_stack((stacked, target))
        correct_combined = np.array(
            [
                # First bin, the failure at time=1 of patient with id=1.
                [0.1, 0.0, 1.0, 0.0, 0.0, 1.0],  # Patient 1's covariates, bin 1/3, fail
                [0.5, 0.0, 1.0, 0.0, 0.0, 0.0],  # Patient 2's covariates, bin 1/3, ok
                [0.7, 1.0, 1.0, 0.0, 0.0, 0.0],  # Patient 3's covariates, bin 1/3, ok
                # Second bin, the failure at time=4 of patient with id=3.
                # Note that patient 2 has changed covariates, at time=3.
                [0.5, 1.0, 0.0, 1.0, 0.0, 0.0],  # Patient 2's covariates, bin 2/3, ok
                [0.7, 1.0, 0.0, 1.0, 0.0, 1.0],  # Patient 3's covariates, bin 2/3, fail
                # Third bin, the failure at time=15 of patient with id=2.
                [0.5, 1.0, 0.0, 0.0, 1.0, 1.0],  # Patient 2's covariates, bin 3/3, fail
            ],
            dtype=float,
        )

        np.testing.assert_array_equal(combined, correct_combined)

    def test_stack_lifelines(self) -> None:
        """
        Validates the time-varying stack function using a lifelines data set.
        The input dataset is a toy example from lifelines.
        The solution has been created by hand.
        """

        data = lifelines.datasets.load_dfcv()
        ids = data["id"].to_numpy()
        covariates = data[["group", "z"]].to_numpy()
        start_times = data["start"].to_numpy()
        end_times = data["stop"].to_numpy()
        failed = data["event"].to_numpy()
        time_bins = np.array([0, 2, 4, 6, 8, 10, 12])

        stacked, target = stack_time_varying(
            ids=ids,
            covariates=covariates,
            start_times=start_times,
            end_times=end_times,
            events=failed,
            time_bins=time_bins,
        )

        combined = np.column_stack((stacked, target))
        correct_combined = np.array(
            [
                [1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0],
                [1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [1.0, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [0.0, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
                [1.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0],
                [1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
                [1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
                [0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
                [0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
                [1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0],
                [1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
                [0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0],
                [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
                [0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
                [0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
                [1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0],
                [0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0],
                [0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0],
                [0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0],
            ],
            dtype=float,
        )

        np.testing.assert_array_equal(combined, correct_combined)

    def test_failure_at_end_times(self) -> None:
        """
        Validates that failures are recorded at the end of a time bin.
        The data and the solution have been created by hand.
        """
        ids = np.array([1, 1, 1], dtype=int)
        covariates = np.array([[70], [80], [60]], dtype=float)
        start_times = np.array([0, 50, 100], dtype=float)
        end_times = np.array([50, 100, 150], dtype=float)
        failed = np.array([0, 0, 1], dtype=float)
        time_bins = np.array([0, 90, 120, 140, 160], dtype=float)

        stacked, target = stack_time_varying(
            ids=ids,
            covariates=covariates,
            start_times=start_times,
            end_times=end_times,
            events=failed,
            time_bins=time_bins,
        )

        combined = np.column_stack((stacked, target))
        correct_combined = np.array(
            [
                [70.0, 1.0, 0.0, 0.0, 0.0, 0.0],
                [80.0, 0.0, 1.0, 0.0, 0.0, 0.0],
                [60.0, 0.0, 0.0, 1.0, 0.0, 0.0],
                [60.0, 0.0, 0.0, 0.0, 1.0, 1.0],
            ]
        )

        np.testing.assert_array_equal(combined, correct_combined)
