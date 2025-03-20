"""
Implementation of the Schoenfeld residuals functionality
"""

from __future__ import annotations

import mpyc.random
import numpy as np
import numpy.typing as npt
import pandas as pd
from mpyc.runtime import mpc
from mpyc.sectypes import SecureFixedPoint, SecureFixedPointArray


def load_data(raw_data: pd.DataFrame, coefficients: pd.DataFrame) -> tuple[
    npt.NDArray[np.float64],
    npt.NDArray[np.int_],
    npt.NDArray[np.int_],
    npt.NDArray[np.float64],
]:
    """
    Load the party's dataset from a local file.
    The model coefficients are assumed to have been calculated and known to all parties.
    In this example, there are 2 parties: Alice and Bob who both have a part of the data.

    :param raw_data: The party's unprocessed dataset
    :param coefficients: The parameters that have been computed in the main Cox model
    :return: The dataset corresponding to that party
    """

    raw_data = raw_data.sort_values(by="time").reset_index()
    covariates = raw_data[["age", "sex", "ph.karno"]]
    times = raw_data["time"]
    events = raw_data["event"]

    return (
        covariates.to_numpy(),
        times.to_numpy(),
        events.to_numpy(),
        coefficients.to_numpy()[0],
    )


def preprocess_data(
    covariates: npt.NDArray[np.float64],
    times: npt.NDArray[np.int_ | np.float64],
    events: npt.NDArray[np.int_],
) -> tuple[
    npt.NDArray[np.float64],
    npt.NDArray[np.float64 | np.int_],
    npt.NDArray[np.int_ | np.float64],
]:
    """
    Each party prepares their data, so it can be used jointly.
    The times are perturbed by a small random value, so that they are unique.
    Then the perturbed times are sorted along with the corresponding events and covariates.

    :param covariates: The covariates of the dataset
    :param times: The times at which the events take place
    :param events: The type of the event (0 for censoring, 1 for failure)
    :return: The sorted covariates, times and failure times
    """

    # Sort data by event times
    n_obs = len(times)
    noise = np.random.normal(loc=0, scale=1e-3, size=n_obs)
    times = times + noise

    sorted_indices = np.argsort(times)
    covariates = covariates[sorted_indices]
    times = times[sorted_indices]
    events = events[sorted_indices]

    failure_times = np.array(times[events == 1])

    return covariates, times, failure_times


def precomputation(
    covariates: npt.NDArray[np.float64],
    times: npt.NDArray[np.int_ | np.float64],
    coefficients: npt.NDArray[np.float64],
    my_failures: npt.NDArray[np.int_ | np.float64],
    failure_times: npt.NDArray[np.int_ | np.float64],
    tolerance: float = 1e-3,
) -> tuple[npt.NDArray[np.float64], npt.NDArray[np.float64], npt.NDArray[np.float64]]:
    """
    Each party does these precomputations, for which it does not need data of others,
    only the list of failure times.
    The hazards and the weights are computed from the covariates and the trained model parameters.
    The hazards and weights are only needed at the failure times.
    The party also puts the correct covariates in the covariate vector
    if it recognizes a failure time as its own.

    :param covariates: The covariates for each party
    :param times: The event times for each party
    :param coefficients: The coefficients of the trained model
    :param my_failures: The failure times for each party
    :param failure_times: The shared complete list of failure times
    :param tolerance: The absolute tolerance allowed in recognizing own failure times
    :return: The hazard vector, weight vector and covariate vector
    """

    # Compute the predicted hazards
    hazards = np.exp(covariates @ coefficients)

    # Compute the weights (pointwise column multiplications)
    weights = (covariates.T * hazards).T

    n_cov = len(coefficients)
    hazard_vector = []
    weight_vector = []
    covariate_vector = []

    for failure in failure_times:
        hazard = 0
        weight = np.zeros(n_cov)

        for idx, time in enumerate(times):
            if time >= failure - tolerance:
                hazard += hazards[idx]
                weight += weights[idx]

        hazard_vector.append(hazard)
        weight_vector.append(weight)

        if np.any(np.abs(my_failures - failure) < tolerance):
            my_idx = np.where(np.abs(times - failure) < tolerance)[0][0]
            covariate_vector.append(covariates[my_idx])
        else:
            covariate_vector.append(np.zeros(n_cov))

    return np.array(hazard_vector), np.array(weight_vector), np.array(covariate_vector)


def share_failures(
    failures: list[list[SecureFixedPoint]],
    secfxp: type[SecureFixedPoint] = mpc.SecFxp(32, 16),
) -> list[SecureFixedPoint]:
    """
    Each party shares the times at which their failures occur,
    without having to publish their times.
    The full list of failures is randomly permuted before publishing,
    so no ownership information is leaked.

    :param failures: The failure times corresponding to each of the parties
    :param secfxp: The type used for secure fixed point numbers
    :return: The failure of all parties combined, in a random order
    """

    all_failures: list[SecureFixedPoint] = sum(failures, [])
    mpyc.random.shuffle(secfxp, all_failures)

    return all_failures


def mpc_schoenfeld_residuals(
    hazards: list[SecureFixedPointArray],
    weights: list[SecureFixedPointArray],
    covariates: list[SecureFixedPointArray],
    secfxp: type[SecureFixedPoint] = mpc.SecFxp(32, 16),
) -> SecureFixedPointArray:
    """
    The actual computation that takes place in the MPC domain.
    Due to the precomputations, only three sums have to be computed:
    of the covariate, hazard and weight vector.
    After this, the expected covariates are the elementwise division of the weights by the hazards.
    The residuals are then the difference of the actual covariates and the expected covariates.

    :param hazards: The hazard vector for each party
    :param weights: The weight vector for each party
    :param covariates: The covariate vector for each party
    :param secfxp: The type used for secure fixed point numbers
    :return: The Schoenfeld residuals of the entire dataset
    """

    start = secfxp.array(np.zeros(1))
    total_covariates = sum(covariates, start=start)
    total_hazards = sum(hazards, start=start)
    total_weights = sum(weights, start=start)

    expected_covariates = (total_weights.T / total_hazards).T

    residuals = total_covariates - expected_covariates

    return residuals
