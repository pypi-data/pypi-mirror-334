"""
Test suite for testing the consistency of the statistics function.
"""

from __future__ import annotations

import asyncio

import numpy as np
import pandas as pd
import pytest
from lifelines import CoxPHFitter

from tno.mpc.communication import Pool

from tno.fl.protocols.cox_regression.client import Client
from tno.fl.protocols.cox_regression.server import Server


@pytest.mark.asyncio
async def test_statistics(http_pool_trio: tuple[Pool, Pool, Pool]) -> None:
    """
    Run the Cox regression with the Rotterdam example.
    Tests the implementation against the CoxPHFitter in the lifelines package.

    :param http_pool_trio: communication pool fixture for 3 parties
    """
    # Create Pool
    server_pool = http_pool_trio[0]
    client1_pool = http_pool_trio[1]
    client2_pool = http_pool_trio[2]
    server_name = "local0"

    # Get data for client 1
    csv_data_alice = pd.read_csv("examples/rotterdam/data_alice.csv")
    covariates_1 = csv_data_alice[
        ["age", "grade", "nodes", "pgr", "er", "meno", "hormon"]
    ].to_numpy()
    times_1 = csv_data_alice["dtime"].to_numpy()
    events_1 = csv_data_alice["death"].to_numpy()

    # Get data for client 2
    csv_data_bob = pd.read_csv("examples/rotterdam/data_bob.csv")
    covariates_2 = csv_data_bob[
        ["age", "grade", "nodes", "pgr", "er", "meno", "hormon"]
    ].to_numpy()
    times_2 = csv_data_bob["dtime"].to_numpy()
    events_2 = csv_data_bob["death"].to_numpy()

    # Run the protocol
    server = Server(server_pool, n_time_bins=75, max_iter=10)
    client1 = Client(client1_pool, max_iter=10, server_name=server_name)
    client2 = Client(client2_pool, max_iter=10, server_name=server_name)

    await asyncio.gather(
        server.run(),
        client1.run(covariates_1, times_1, events_1),
        client2.run(covariates_2, times_2, events_2),
    )

    statistics = await asyncio.gather(
        server.compute_statistics(),
        client1.compute_statistics(),
        client2.compute_statistics(),
    )

    # Parse results
    standard_errors = [stat["se"] for stat in statistics[1]]
    z_values = [stat["z"] for stat in statistics[1]]
    p_values = [stat["p"] for stat in statistics[1]]

    standard_errors2 = [stat["se"] for stat in statistics[2]]
    z_values2 = [stat["z"] for stat in statistics[2]]
    p_values2 = [stat["p"] for stat in statistics[2]]

    # Run baseline coxph fitter
    csv_data = pd.read_csv("examples/rotterdam/data.csv")
    data = csv_data[
        ["age", "grade", "nodes", "pgr", "er", "meno", "hormon", "dtime", "death"]
    ]
    cph = CoxPHFitter()
    cph.fit(data, "dtime", "death")
    print(cph.summary)

    # Tests both client have equal statistics
    assert np.array_equal(standard_errors, standard_errors2)
    assert np.array_equal(z_values, z_values2)
    assert np.array_equal(p_values, p_values2)

    # Compare with lifelines
    assert np.isclose(
        standard_errors,
        cph.summary["se(coef)"].to_list(),
        rtol=5e-02,
        atol=5e-02,
    ).all()
    assert np.isclose(
        p_values,
        cph.summary["p"].to_list(),
        rtol=5e-01,
        atol=2e-02,
    ).all()
