"""File with ridge regression model algorithm."""

# Third-party libraries
import numpy as np

# First-party libraries
from pamm.algorithms.regression.regression_model import RegressionAlgorithm


class RidgeRegressionAlgorithm(RegressionAlgorithm):
    def fit(self, x: np.ndarray, y: np.ndarray, alpha: float = 0.1) -> None:
        """Fit model.

        Args:
            x (np.ndarray): matrix of regressors
            y (np.ndarray): matrix a teacher
            alpha (float): regularization parameter
        """
        x = self._add_bias(x)
        i = np.eye(x.shape[1])
        tmp = np.linalg.inv(x.T @ x + alpha * i) @ x.T @ y
        self._beta = tmp[int(self._fit_bias) :]
        self._bias = tmp[0][0] * int(self._fit_bias)
