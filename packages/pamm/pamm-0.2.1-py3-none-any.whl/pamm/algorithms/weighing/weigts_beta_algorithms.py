"""File with algorithms for calculate matrix of trust beta coefficients."""

# Standard Library

# Third-party libraries
# Third Party Library
import numpy as np


def max_truth(data_table: np.ndarray) -> np.ndarray:
    size_to_append = 1000000
    beta_vector = np.where(np.abs(data_table.T) > 0, size_to_append, 0)[0]
    return np.diag(beta_vector)
