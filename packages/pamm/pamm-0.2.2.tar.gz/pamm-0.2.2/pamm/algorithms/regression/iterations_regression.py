"""File with regression model algorithm on two-stage least sqares."""

# Third-party libraries
import numpy as np

# First-party libraries
from pamm.algorithms.regression.regression_model import RegressionAlgorithm


class IterationRegressionAlgorithm(RegressionAlgorithm):
    def _add_bias(self, x: np.array) -> np.array:
        return np.hstack([np.ones((x.shape[0], 1)), x])

    def fit(self, x: np.ndarray, y: np.ndarray) -> None:
        """Fit model.

        Args:
            x (np.ndarray): matrix of endogenous regressors (features)
            y (np.ndarray): matrix a teacher
        """

        remnant = y
        x = self._add_bias(x)
        rows, cols = x.shape
        tmp = np.zeros([cols, 1])

        for col in range(1, cols):
            x_i = x[:, col].reshape([rows, 1])
            x_i_b = self._add_bias(x_i)
            beta = np.linalg.inv(x_i_b.T @ x_i_b) @ x_i_b.T @ remnant
            tmp[col][0] = beta[1][0]
            remnant = remnant - x_i * beta[1][0]

        tmp[0][0] = remnant.mean()
        self._beta = tmp[int(self._fit_bias) :]
        self._bias = tmp[0][0] * int(self._fit_bias)
