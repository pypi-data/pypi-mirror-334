"""Module with statistick methods between two time-series."""

# Third-party libraries
import numpy as np


def mse(major_ts: np.array, minor_ts: np.array) -> float:
    """Calculate mean squared error between 2 metricks.

    Args:
        major_ts (np.array): original data vector.
        minor_ts (np.array): predicted data vector.

    Returns:
        float: mean squared  error.
    """
    return ((major_ts - minor_ts) ** 2).mean()


def rmse(major_ts: np.array, minor_ts: np.array) -> float:
    """Calculate root mean squared error between 2 metricks.

    Args:
        major_ts (np.array): original data vector.
        minor_ts (np.array): predicted data vector.

    Returns:
        float: root mean squared error.
    """
    return np.sqrt(mse(major_ts, minor_ts))


def mae(major_ts: np.array, minor_ts: np.array) -> float:
    """Calculate mean absolute error between 2 metricks.

    Args:
        major_ts (np.array): original data vector.
        minor_ts (np.array): predicted data vector.

    Returns:
        float: absolute squared error.
    """
    return np.mean(np.abs(major_ts - minor_ts))


def mspe(major_ts: np.array, minor_ts: np.array) -> float:
    """Calculate mean squared percentable error between 2 metricks.

    Args:
        major_ts (np.array): original data vector.
        minor_ts (np.array): predicted data vector.

    Returns:
        float: mean squared percentable error.
    """

    return 100 * (((major_ts - minor_ts) / major_ts) ** 2).mean()


def mape(major_ts: np.array, minor_ts: np.array) -> float:
    """Calculate mean absolute percecentable error between 2 metricks.

    Args:
        major_ts (np.array): original data vector.
        minor_ts (np.array): predicted data vector.

    Returns:
        float: mean absolute percecentable error.
    """
    return 100 * np.mean(np.abs((major_ts - minor_ts) / major_ts))


def smape(major_ts: np.array, minor_ts: np.array) -> float:
    """Calculate symmetrical mean absolute percecentable error between 2 metricks.

    Args:
        major_ts (np.array): original data vector.
        minor_ts (np.array): predicted data vector.

    Returns:
        float: symmetrical mean absolute percecentable error.
    """
    return 100 * np.mean(
        np.abs(major_ts - minor_ts) / ((np.abs(minor_ts) + np.abs(major_ts)) / 2)
    )


def mre(major_ts: np.array, minor_ts: np.array) -> float:
    """Calculate relative mean error between 2 metricks.

    Args:
        major_ts (np.array): original data vector.
        minor_ts (np.array): predicted data vector.

    Returns:
        float: relative mean error.
    """
    return np.mean(np.abs(major_ts - minor_ts) / np.abs(major_ts))


def rmsle(major_ts: np.array, minor_ts: np.array) -> float:
    """Calculate root mean squared logarithmic error between 2 metricks.

    Args:
        major_ts (np.array): original data vector.
        minor_ts (np.array): predicted data vector.

    Returns:
        float: root mean squared logarithmic error.
    """
    return np.sqrt(np.mean((np.log(major_ts + 1) - np.log(minor_ts + 1)) ** 2))


def corr(major_ts: np.array, minor_ts: np.array) -> float:
    """Calculate correlation coefficient.

    Args:
        major_ts (np.array): original data vector.
        minor_ts (np.array): predicted data vector.

    Returns:
        float: correlation coefficient.
    """
    return np.corrcoef(major_ts, minor_ts, rowvar=False)[0, 1]


def r2(major_ts: np.array, minor_ts: np.array) -> float:
    """Calculate determination coefficient.

    Args:
        major_ts (np.array): original data vector.
        minor_ts (np.array): predicted data vector.

    Returns:
        float: determination coefficient.
    """
    s_res = np.sum((major_ts - minor_ts) ** 2)
    s_tot = np.sum((major_ts - major_ts.mean()) ** 2)
    return 1 - s_res / s_tot


def adjusted_r2(major_ts: np.array, minor_ts: np.array, count_features: int) -> float:
    """Calculate adjusted determination coefficient.

    Args:
        major_ts (np.array): original data vector.
        minor_ts (np.array): predicted data vector.
        count_features (int): count features in model.
        count_observe (int): count observers in ts.

    Returns:
        float: adjusted determination coefficient.
    """
    count_observe = major_ts.shape[0]
    return 1 - (mse(major_ts, minor_ts) / (count_observe - count_features)) / (
        ((major_ts - major_ts.mean()) ** 2).mean() / (count_observe - 1)
    )
