"""File with algorithms for calculate matrix of trust data."""

# Standard Library

# Third-party libraries
# Third Party Library
import numpy as np


def equal(data_table: np.ndarray) -> np.ndarray:
    return np.eye(data_table.shape[0])


def time_booster(data_table: np.ndarray) -> np.ndarray:
    return np.diag([x for x in range(0, data_table.shape[0])])


def inversely(data_table: np.ndarray) -> np.ndarray:
    return np.diag(1 / data_table[:, 0])


def big_target(data_table: np.ndarray) -> np.ndarray:
    return np.diag(np.abs(data_table[:, 0] - np.mean(data_table)))


def ln_algorithm(data_table: np.ndarray) -> np.ndarray:
    return np.diag([np.log(x) for x in range(1, data_table.shape[0] + 1)])
