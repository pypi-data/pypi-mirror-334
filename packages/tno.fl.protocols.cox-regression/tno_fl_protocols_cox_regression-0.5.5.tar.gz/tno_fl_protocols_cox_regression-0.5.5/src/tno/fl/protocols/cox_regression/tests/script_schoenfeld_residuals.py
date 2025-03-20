"""
Tests for the Schoenfeld residuals.
Called by test_schoenfeld_residuals.py to test with multiple parties.
"""

from __future__ import annotations

from typing import Any, cast

import numpy as np
from mpyc.runtime import mpc
from mpyc.sectypes import SecureFixedPoint, SecureInteger
from numpy.typing import NDArray

from tno.fl.protocols.cox_regression.schoenfeld_residuals import (
    mpc_schoenfeld_residuals,
    precomputation,
    preprocess_data,
    share_failures,
)

test_data = {
    0: (  # Party 0
        np.array([[0.3, 2.1], [0.4, 2.5], [0.6, 1.7], [0.7, 2.3]]),  # Covariates
        np.array([1, 3, 21, 33]),  # Times
        np.array([0, 1, 0, 1]),  # Events
        np.array([0.0013, -0.0472]),  # (Arbitrary) coefficients
    ),
    1: (  # Party 1
        np.array([[0.6, 2.0], [0.2, 1.9], [0.1, 1.3], [0.9, 2.1]]),  # Covariates
        np.array([7, 15, 29, 36]),  # Times
        np.array([1, 1, 0, 1]),  # Events
        np.array([0.0013, -0.0472]),  # (Arbitrary) coefficients
    ),
    2: (  # Party 2
        np.array([[0.5, 1.8], [0.7, 2.3], [0.4, 1.0], [0.8, 2.4]]),  # Covariates
        np.array([8, 11, 22, 25]),  # Times
        np.array([1, 0, 0, 0]),  # Events
        np.array([0.0013, -0.0472]),  # (Arbitrary) coefficients
    ),
}


async def main(
    secint: type[SecureInteger] = mpc.SecInt(32),
    secfxp: type[SecureFixedPoint] = mpc.SecFxp(32, 16),
) -> None:
    """
    Main loop of the test case.
    The Schoenfeld residuals are calculated in the MPC protocol,
    then compared to the known precomputed correct values.

    :param secint: The type used for secure integers
    :param secfxp: The type used for secure fixed point numbers
    """
    async with mpc:
        party_id = mpc.pid

        # Preprocess the data
        covariates, times, events, coefficients = test_data[party_id]
        processed_covariates, processed_times, processed_failures = preprocess_data(
            covariates, times, events
        )

        # Compute single public list of all failure times
        lengths = mpc.input(secint(len(events)))
        max_length = await mpc.output(mpc.max(lengths))
        padded_failures = cast(
            list[Any],
            np.append(
                processed_failures,
                np.zeros(max_length - len(processed_failures), dtype=float),
            ).tolist(),
        )
        my_failures: list[list[SecureFixedPoint]] = mpc.input(
            [secfxp(f) for f in padded_failures]
        )

        our_failures = await mpc.output(share_failures(my_failures))
        all_failures = np.array(our_failures)
        shared_failures = np.sort(all_failures[all_failures > 0])

        # Perform the necessary precomputations
        hazard_vector, weight_vector, covariate_vector = precomputation(
            processed_covariates,
            processed_times,
            coefficients,
            processed_failures,
            shared_failures,
        )

        mpc_hazards = mpc.input(secfxp.array(hazard_vector))
        mpc_weights = mpc.input(secfxp.array(weight_vector))
        mpc_covariates = mpc.input(secfxp.array(covariate_vector))

        result = mpc_schoenfeld_residuals(mpc_hazards, mpc_weights, mpc_covariates)
        mpc_residuals = cast(NDArray[Any], await mpc.output(result))

        # Known desired outcome for this test
        benchmark_residuals = np.array(
            [
                [-0.13368605, 0.5730097],
                [0.05333604, 0.12863607],
                [-0.04077579, -0.05716282],
                [-0.32437301, 0.09649477],
                [-0.100485, 0.100485],
                [0.0, 0.0],
            ]
        )

        assert mpc_residuals.shape == benchmark_residuals.shape, (
            "Resulting dimensions did not match target. "
            "Please run this script with MPyC using the argument -M3."
        )
        assert np.allclose(benchmark_residuals, mpc_residuals, rtol=1e-3, atol=1e-3)


if __name__ == "__main__":
    mpc.run(main())
