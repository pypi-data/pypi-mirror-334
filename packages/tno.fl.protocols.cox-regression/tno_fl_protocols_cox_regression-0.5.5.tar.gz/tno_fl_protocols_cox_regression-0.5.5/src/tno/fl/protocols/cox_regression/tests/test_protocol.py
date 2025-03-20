"""
Test suite for testing the correctness of the protocol.
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
async def test_protocol(http_pool_trio: tuple[Pool, Pool, Pool]) -> None:
    """
    Run the Cox regression with the Rotterdam example.
    Tests the implementation against the lifelines CoxPHFitter module.

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
    server = Server(server_pool, n_time_bins=100, max_iter=10)
    client1 = Client(client1_pool, max_iter=10, server_name=server_name)
    client2 = Client(client2_pool, max_iter=10, server_name=server_name)

    models = await asyncio.gather(
        server.run(),
        client1.run(covariates_1, times_1, events_1),
        client2.run(covariates_2, times_2, events_2),
    )

    # Run baseline coxph fitter
    csv_data = pd.read_csv("examples/rotterdam/data.csv")
    data = csv_data[
        ["age", "grade", "nodes", "pgr", "er", "meno", "hormon", "dtime", "death"]
    ]
    cph = CoxPHFitter()
    cph.fit(data, "dtime", "death")

    # Tests
    assert np.array_equal(models[1], models[2])
    assert np.isclose(
        models[1][:7],
        cph.params_.to_list(),
        rtol=2e-02,
        atol=2e-02,
        equal_nan=False,
    ).all()
