"""
Client module for cox regression
"""

from __future__ import annotations

import logging
from typing import cast

import numpy as np

from tno.fl.protocols.logistic_regression.client import Client as LogRegClient
from tno.fl.protocols.logistic_regression.client import ModelType
from tno.mpc.communication import Pool

from tno.fl.protocols.cox_regression import msg_ids, survival_stacking
from tno.fl.protocols.cox_regression.survival_stacking import (
    CovariatesType,
    DataType,
    EventsType,
    IdsType,
    TargetType,
    TimeBinType,
    TimesType,
)

logger = logging.getLogger(__name__)


class Client:
    """
    The client class, representing data owning clients in the learning process.
    Based on logistic regression client.
    """

    def __init__(
        self,
        pool: Pool,
        max_iter: int = 25,
        server_name: str = "server",
    ) -> None:
        """
        Initializes the client.

        :param pool: The communication pool.
        :param max_iter: The max number of epochs
        :param server_name: The name of the server in the communication pool
        """
        self.pool = pool
        self.server_name = server_name
        self.log_reg_solver = LogRegClient(
            pool=pool, max_iter=max_iter, server_name=server_name
        )
        # Placeholders for stacked data
        self._stacked_data_: DataType | None = None
        self.n_covariates_: int = 0
        self._stacked_target_: TargetType | None = None
        self._model_: ModelType | None = None

    @property
    def stacked_data_(self) -> DataType:
        """
        Return the stacked data.

        :return: the stacked data.
        :raises ValueError: when stacked data is not set.
        """
        if self._stacked_data_ is None:
            raise ValueError("Stacked data not set. First run the Cox Regression.")
        return self._stacked_data_

    @property
    def stacked_target_(self) -> TargetType:
        """
        Return the stacked target vector.

        :return: the stacked target vector.
        :raises ValueError: when stacked target is not set.
        """
        if self._stacked_target_ is None:
            raise ValueError("Stacked target not set. First run the Cox Regression.")
        return self._stacked_target_

    @property
    def model_(self) -> ModelType:
        """
        Return the fitted model.

        :return: the fitted model
        :raises ValueError: when model is not yet computed.
        """
        if self._model_ is None:
            raise ValueError("Model not set. First run the Cox Regression.")
        return self._model_

    async def _compute_time_bins(self, times: TimesType) -> TimeBinType:
        """
        Compute the time bins for the stacking.
        This is done by computing the local maximum event time to the server.
        The server returns the time bin division to the clients.

        :param times: The times at the local clients
        :return: The global maximum event time
        """
        # Share local max time with server
        local_max_time = times.max(initial=0)
        await self.pool.send(
            self.server_name, message=local_max_time, msg_id=msg_ids.LOCAL_MAX_TIME
        )
        # Receive and return time bins from server
        return cast(
            TimeBinType,
            await self.pool.recv(self.server_name, msg_id=msg_ids.TIME_BINS),
        )

    async def run(
        self,
        covariates: CovariatesType,
        times: TimesType,
        events: EventsType,
    ) -> ModelType:
        """
        Perform the learning process.

        :param covariates: The covariates of the patients. Can have multiple columns.
        :param times: The failure/censoring times.
        :param events: The event indicators. Should contain boolean values.
        :return: The resulting model.
        """
        # Set default value for time bins
        logger.info("Computing time bins..")
        time_bins = await self._compute_time_bins(times)
        self.n_covariates_ = covariates.shape[1]

        # Stack the data
        logger.info("Stacking the data..")
        self._stacked_data_, self._stacked_target_ = survival_stacking.stack(
            covariates=covariates,
            times=times,
            events=events,
            time_bins=time_bins,
        )
        logger.info("Finished stacking, starting Logistic Regression")

        # Perform the logistic regression
        logger.info("Running Logistic Regression..")
        self._model_ = await self.log_reg_solver.run(
            self._stacked_data_.astype(np.float64), self._stacked_target_
        )

        return self._model_

    async def run_time_varying(
        self,
        ids: IdsType,
        covariates: CovariatesType,
        start_times: TimesType,
        end_times: TimesType,
        events: EventsType,
    ) -> ModelType:
        """
        Perform the learning process.

        :param ids: The patient ids. Can be used to specify time-varying covariates. The id is unique
            per patient and a patient can have multiple rows. However, a patient id can have only one
            failure.
        :param covariates: The covariates of the patients. Can have multiple columns.
        :param start_times: The start time of the interval.
        :param end_times: The end time of the interval.
        :param events: The event indicators. Should contain boolean values.
        :return: The resulting model.
        """
        # Set default value for time bins
        logger.info("Computing time bins..")
        time_bins = await self._compute_time_bins(end_times)
        self.n_covariates_ = covariates.shape[1]

        # Stack the data
        logger.info("Stacking the data..")
        (
            self._stacked_data_,
            self._stacked_target_,
        ) = survival_stacking.stack_time_varying(
            ids, covariates, start_times, end_times, events, time_bins
        )
        logger.info("Finished stacking, starting Logistic Regression")

        # Perform the logistic regression
        logger.info("Running Logistic Regression..")
        self._model_ = await self.log_reg_solver.run(
            self._stacked_data_.astype(np.float64), self._stacked_target_
        )

        return self._model_

    async def compute_statistics(
        self, include_bins: bool = False
    ) -> list[dict[str, float]]:
        """
        Compute statistics for each coefficient: standard error, z-value and p-value.

        :param include_bins: Whether to include parameters for the time bins.
        :return: A list containing a dictionary for each covariate. The dictionary contains three values:
            'se' containing the standard error,
            'z' containing z-value (Wald statistic)
            'p' containing the p-value.
        """
        statistics = await self.log_reg_solver.compute_statistics(
            self.stacked_data_.astype(np.float64), self.stacked_target_, self.model_
        )
        if not include_bins:
            statistics = statistics[: self.n_covariates_]
        return statistics
