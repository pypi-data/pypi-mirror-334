# pylint: disable=unused-argument,too-many-arguments

from typing import Literal

import numpy as np
from numpy.typing import NDArray

def lowess(
    endog: NDArray[np.float64],
    exog: NDArray[np.float64],
    frac: float = 2.0 / 3.0,
    it: int = 3,
    delta: float = 0.0,
    xvals: NDArray[np.float64] | None = None,
    is_sorted: bool = False,
    missing: Literal["drop"] | Literal["raise"] = "drop",
    return_sorted: bool = True,
) -> NDArray[np.float64]: ...
