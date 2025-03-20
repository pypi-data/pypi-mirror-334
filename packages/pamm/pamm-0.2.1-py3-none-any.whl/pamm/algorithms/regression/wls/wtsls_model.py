"""File with regression model algorithm on two-stage least sqares."""

# Third-party libraries
import numpy as np

# First-party libraries
from pamm.algorithms.regression.regression_model import RegressionAlgorithm


class WeightedTwoStageLeastSquaresAlgorithm(RegressionAlgorithm):
    def fit(self, x: np.ndarray, z: np.array, w: np.array, y: np.ndarray) -> None:
        """Fit model.

        Args:
            x (np.ndarray): matrix of endogenous regressors (features)
            z (np.ndarray): matrix of exogenous regressors (tools)
            w (np.ndarray): matrix weights of exogenous regressors
            y (np.ndarray): matrix a teacher
        """
        x = self._add_bias(x)
        p = w @ z @ np.linalg.inv(z.T @ w @ z) @ z.T @ w
        tmp = np.linalg.inv(x.T @ p @ x) @ x.T @ p @ y
        self._beta = tmp[int(self._fit_bias) :]
        self._bias = tmp[0][0] * int(self._fit_bias)
