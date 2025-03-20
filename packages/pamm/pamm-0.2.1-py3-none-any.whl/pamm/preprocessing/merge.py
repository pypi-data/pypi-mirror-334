# Standard Library
from typing import Literal

# Third-party libraries
import numpy as np


def forward(major_ts: np.ndarray, minor_ts: np.ndarray, trust: int) -> np.ndarray:
    """Reterned values from timeseries nearest forward in time.

    Args:
        major_ts (np.ndarray): time-series original.
        minor_ts (np.ndarray): time-series for merge.
        trust (int): trust interval.

    Returns:
        np.ndarray: merged values.
    """
    arr = np.empty(major_ts.shape)
    indexes = np.searchsorted(minor_ts[:, 0], major_ts[:, 0], side="left")
    arr[:, 0] = np.take(minor_ts[:, 0], [indexes], mode="wrap") - major_ts[:, 0]
    arr[:, 1] = np.take(minor_ts[:, 1], [indexes], mode="wrap")
    arr = arr.astype(float)
    arr[arr[:, 0] > trust] = np.nan
    arr[arr[:, 0] < 0] = np.nan
    return arr


def backward(major_ts: np.ndarray, minor_ts: np.ndarray, trust: int) -> np.ndarray:
    """Reterned values from timeseries nearest back in time.

    Args:
        major_ts (np.ndarray): time-series original.
        minor_ts (np.ndarray): time-series for merge.
        trust (int): trust interval.

    Returns:
        np.ndarray: merged values.
    """
    arr = np.empty(major_ts.shape)
    indexes = np.searchsorted(minor_ts[:, 0], major_ts[:, 0], side="right") - 1
    arr[:, 0] = major_ts[:, 0] - np.take(minor_ts[:, 0], [indexes], mode="wrap")
    arr[:, 1] = np.take(minor_ts[:, 1], [indexes], mode="wrap")
    arr = arr.astype(float)
    arr[arr[:, 0] > trust] = np.nan
    arr[arr[:, 0] < 0] = np.nan
    return arr


def nearest(major_ts: np.ndarray, minor_ts: np.ndarray, trust: int) -> np.ndarray:
    """Reterned values from timeseries nearest in time.

    Args:
        major_ts (np.ndarray): time-series original.
        minor_ts (np.ndarray): time-series for merge.
        trust (int): trust interval.

    Returns:
        np.ndarray: merged values.
    """
    indexes = np.searchsorted(minor_ts[:, 0], major_ts[:, 0], "right")
    left_diff = np.abs(
        np.take(minor_ts[:, 0], indexes - 1, mode="wrap") - major_ts[:, 0]
    )
    right_diff = np.abs(np.take(minor_ts[:, 0], indexes, mode="wrap") - major_ts[:, 0])
    nearest_indexes = np.where(left_diff > right_diff, indexes, indexes - 1)
    arr = minor_ts[nearest_indexes]
    arr[:, 0] = np.abs(arr[:, 0] - major_ts[:, 0])
    arr = arr.astype(float)
    arr[arr[:, 0] > trust] = np.nan
    return arr


def sync_ts(
    major_ts: np.ndarray,
    minor_ts: np.ndarray,
    method: Literal["backward", "forward", "nearest"] = "backward",
    trust: int = np.inf,
) -> np.ndarray:
    """_summary_

    Args:
        major_ts (np.ndarray): _description_
        minor_ts (np.ndarray): _description_
        method (Literal[backward, forward, nearest], optional): _description_. Defaults to 'backward'.
        trust (int, optional): _description_. Defaults to np.inf.

    Returns:
        np.ndarray: merged data
    """

    match method:
        case "backward":
            return backward(major_ts=major_ts, minor_ts=minor_ts, trust=trust)

        case "forward":
            return forward(major_ts=major_ts, minor_ts=minor_ts, trust=trust)

        case "nearest":
            return nearest(major_ts=major_ts, minor_ts=minor_ts, trust=trust)
