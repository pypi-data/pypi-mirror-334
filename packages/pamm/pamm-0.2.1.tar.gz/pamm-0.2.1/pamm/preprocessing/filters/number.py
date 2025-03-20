# Third-party libraries
import numpy as np


def peccentel_edge(ts: np.ndarray, percentile: float) -> np.ndarray:
    """Delete all values bihind percentel for two edges.

    Args:
        ts (np.ndarray): time-series.
        percentile (float): percentile data.

    Returns:
        np.ndarray: filtered time-series.
    """
    values = ts[:, 1]
    up_percentile = np.percentile(values, percentile)
    low_percentile = np.percentile(values, 100 - percentile)
    mask = (values < up_percentile), (values > low_percentile)
    return ts[np.logical_and(*mask)]


def percentel(ts: np.ndarray, percentile: float) -> np.ndarray:
    """Delete all values bihind percentel.

    Args:
        ts (np.ndarray): time-series.
        percentile (float): percentile data.

    Returns:
        np.ndarray: filtered time-series.
    """
    values = ts[:, 1]
    percent = np.percentile(values, percentile)
    mask = values < percent
    return ts[np.logical_and(*mask)]


def power(ts: np.ndarray, pow: float = 2) -> np.ndarray:
    """Delete all values bihind percentel.

    Args:
        ts (np.ndarray): time-series.
        percentile (float): percentile data.

    Returns:
        np.ndarray: filtered time-series.
    """
    ts[:, 1] = ts[:, 1] ** pow
    return ts


def inside(
    ts: np.ndarray, min: int | None = None, max: int | None = None
) -> np.ndarray:
    """Return values only inside interval.

    Args:
        ts (np.ndarray): time-seriess.
        min (int): start date for drop.
        max (int): end date for drop.

    Returns:
        np.ndarray: filtered time-seriess.
    """
    min = min if min else -np.inf
    max = max if max else np.inf
    values = ts[:, 0]
    mask = (values > min), (values < max)
    return ts[np.logical_and(*mask)]


def moving_average(ts: np.ndarray, window: int) -> np.ndarray:
    """Return values only inside interval.

    Args:
        ts (np.ndarray): time-seriess.
        window (int): sliding window.

    Returns:
        np.ndarray: filtered time-seriess.
    """
    times = np.convolve(ts[:, 0], np.ones(window), "valid") / window
    values = np.convolve(ts[:, 1], np.ones(window), "valid") / window
    # FIXME np.column_stack не нужно транспонировать
    return np.vstack([times, values]).T
