"""
Example usage of the Schoenfeld residuals with two parties.
"""

from __future__ import annotations

import os
from typing import Any, cast

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from mpyc.runtime import mpc
from mpyc.sectypes import SecureFixedPoint, SecureInteger
from statsmodels.nonparametric.smoothers_lowess import lowess

from tno.fl.protocols.cox_regression.schoenfeld_residuals import (
    load_data,
    mpc_schoenfeld_residuals,
    precomputation,
    preprocess_data,
    share_failures,
)


async def main(
    secint: type[SecureInteger] = mpc.SecInt(32),
    secfxp: type[SecureFixedPoint] = mpc.SecFxp(32, 16),
) -> None:
    """
    Main loop of the Schoenfeld calculation.

    :param secint: The type used for secure integers
    :param secfxp: The type used for secure fixed point numbers
    """
    async with mpc:

        party_id = mpc.pid
        current_dir = os.path.dirname(__file__)
        path = f"{current_dir}/data-party-{party_id}.csv"

        # Preprocess the data
        raw_data = pd.read_csv(path)
        raw_coefficients = pd.read_csv(f"{current_dir}/coefficients.csv")
        covariates, times, events, coefficients = load_data(raw_data, raw_coefficients)
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
        mpc_residuals = await mpc.output(result)
        print(f"MPC result, Schoenfeld residuals:\n{mpc_residuals}")

        show_smoothing = True
        residual_names = ("age", "sex", "ph.karno")

        for name, residual in zip(residual_names, np.asarray(mpc_residuals).T):
            plt.clf()
            plt.scatter(shared_failures, residual, s=10, c="b")
            if show_smoothing:
                plt.plot(*lowess(residual, shared_failures).T, c="r")
            os.makedirs(f"{current_dir}/residual_plots", exist_ok=True)
            plt.savefig(f"{current_dir}/residual_plots/schoenfeld_residuals_{name}.png")


if __name__ == "__main__":
    mpc.run(main())
