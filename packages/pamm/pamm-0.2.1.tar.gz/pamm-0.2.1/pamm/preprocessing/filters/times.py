# Third-party libraries
import numpy as np


def set_delay(ts: np.ndarray, delay: int) -> np.ndarray:
    """Add delation for time-series.

    Args:
        ts (np.ndarray): time-seriess.
        delay (int): delay in int format.

    Returns:
        np.ndarray: filtered time-seriess.
    """
    data = ts.copy()
    data[:, 0] = data[:, 0] + delay
    return data


def drop_date(ts: np.ndarray, start: int, end: int) -> np.ndarray:
    """Dropped time interval from time-series.

    Args:
        ts (np.ndarray): time-seriess.
        start (int): start date for drop.
        end (int): end date for drop.

    Returns:
        np.ndarray: filtered time-seriess.
    """
    values = ts[:, 0]
    mask = (values < end), (values > start)
    return ts[np.logical_and(*mask)]
