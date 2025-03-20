"""File with weigthed regression model algorithm."""

# Third-party libraries
import numpy as np

# First-party libraries
from pamm.algorithms.regression.regression_model import RegressionAlgorithm


class WeigthedRegressionAlgorithm(RegressionAlgorithm):
    def fit(self, x: np.ndarray, y: np.ndarray, w: np.ndarray) -> None:
        """Fit model.

        Args:
            x (np.ndarray): matrix of regression
            y (np.ndarray): matrix a teacher data
            w (np.ndarray): matrix of weights
        """
        x = self._add_bias(x)
        tmp = np.linalg.inv(x.T @ w @ x) @ x.T @ w @ y
        self._beta = tmp[int(self._fit_bias) :]
        self._bias = tmp[0][0] * int(self._fit_bias)
