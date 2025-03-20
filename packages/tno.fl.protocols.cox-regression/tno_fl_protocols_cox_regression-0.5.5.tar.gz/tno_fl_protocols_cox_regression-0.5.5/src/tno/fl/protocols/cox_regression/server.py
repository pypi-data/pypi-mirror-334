"""
Server module for cox regression
"""

from __future__ import annotations

import logging

import numpy as np

from tno.fl.protocols.logistic_regression.server import Server as LogRegServer
from tno.mpc.communication import Pool

from tno.fl.protocols.cox_regression import msg_ids
from tno.fl.protocols.cox_regression.survival_stacking import TimeBinType

logger = logging.getLogger(__name__)


class Server:
    """
    The Server class. Responsible for aggregating results of the clients.
    Based on the logistic regression server.
    """

    def __init__(self, pool: Pool, n_time_bins: int, max_iter: int = 25) -> None:
        """
        Initializes the server.

        :param pool: The communication pool.
        :param n_time_bins: The number of time bins to use.
        :param max_iter: The max number of epochs
        """
        self.pool = pool
        self.n_time_bins = n_time_bins
        self.log_reg_solver = LogRegServer(pool=pool, max_iter=max_iter)

    async def _compute_global_max_time(self) -> float:
        """
        Receive local maximum event times and distribute global maximum event time.
        """
        local_max_times = await self.pool.recv_all(msg_id=msg_ids.LOCAL_MAX_TIME)
        return float(max(max_time for _, max_time in local_max_times))

    def _split_time_bins(self, global_max_time: float) -> TimeBinType:
        """
        Compute time bins evenly given a max event time.

        :param global_max_time: The global max event time
        :return: The time bins
        """
        return np.linspace(0, global_max_time + 1, self.n_time_bins)

    async def _compute_time_bins(
        self, time_bins: TimeBinType | None = None
    ) -> TimeBinType:
        """
        Compute time bins, based on the input of the clients.

        :param time_bins: Optional parameter specifying the time bins.
            If None, the bins will be spaced according to the _split_time_bins function.
        :return: The time bins
        :raises ValueError: If time bins are smaller than maximum time.
        """
        global_max_time = await self._compute_global_max_time()
        if time_bins is None:
            return self._split_time_bins(global_max_time)
        if np.max(time_bins) < global_max_time:
            raise ValueError("Global max time is greater than maximum time bin.")
        return time_bins

    async def run(self, time_bins: TimeBinType | None = None) -> None:
        """
        Runs the entire learning process.

        :param time_bins: Optional parameter specifying the time bins.
            If None, the bins will be spaced according to the _split_time_bins function.
        """
        # Compute and distribute the global maximum event time
        logger.info("Computing time bins..")
        time_bins = await self._compute_time_bins(time_bins)
        await self.pool.broadcast(time_bins, msg_ids.TIME_BINS)

        # Perform the logistic regression
        logger.info("Starting Logistic Regression..")
        await self.log_reg_solver.run()

    async def compute_statistics(self) -> None:
        """
        Perform server role in computing the statistics.
        """
        await self.log_reg_solver.compute_statistics()
