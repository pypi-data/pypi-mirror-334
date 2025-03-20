"""
Stubs for the lifelines package
"""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any, List

import numpy as np
import numpy.typing as npt
import pandas as pd

class CoxPHFitter:
    params_: pd.Series[Any]
    summary: pd.DataFrame

    def __init__(
        self,
        baseline_estimation_method: str = "breslow",
        penalizer: float | np.ndarray[Any, Any] = 0.0,
        strata: list[str] | str | None = None,
        l1_ratio: float = 0.0,
        n_baseline_knots: int | None = None,
        knots: list[Any] | None = None,
        breakpoints: list[Any] | None = None,
    ) -> None: ...
    def fit(
        self,
        df: pd.DataFrame,
        duration_col: str | None = None,
        event_col: str | None = None,
        show_progress: bool = False,
        initial_point: np.ndarray[Any, Any] | None = None,
        strata: list[str] | str | None = None,
        weights_col: str | None = None,
        cluster_col: str | None = None,
        robust: bool = False,
        batch_mode: bool | None = None,
        timeline: Iterator[Any] | None = None,
        formula: str | None = None,
        entry_col: str | None = None,
        fit_options: dict[Any, Any] | None = None,
    ) -> CoxPHFitter: ...

class CoxTimeVaryingFitter:
    params_: pd.Series[Any]

    def __init__(
        self,
        alpha: float = 0.05,
        penalizer: float = 0.0,
        l1_ratio: float = 0.0,
        strata: list[Any] | Any = None,
    ) -> None: ...
    def fit(
        self,
        df: pd.DataFrame,
        event_col: str,
        start_col: str = "start",
        stop_col: str = "stop",
        weights_col: str | None = None,
        id_col: str | None = None,
        show_progress: bool = False,
        robust: bool | None = False,
        strata: list[str] | str | None = None,
        initial_point: npt.NDArray[Any] | None = None,
        formula: str | None = None,
        fit_options: dict[str, float] | None = None,
    ) -> CoxTimeVaryingFitter: ...
    def print_summary(
        self,
        decimals: int = 2,
        style: str | None = None,
        columns: list[str] | None = None,
    ) -> str: ...
