"""File with regression model algorithm on two-stage least sqares."""

# Third-party libraries
import numpy as np

# First-party libraries
from pamm.algorithms.regression.regression_model import RegressionAlgorithm


class TwoStageLeastSquaresAlgorithm(RegressionAlgorithm):
    def fit(self, x: np.ndarray, z: np.array, y: np.ndarray) -> None:
        """Fit model.

        Args:
            x (np.ndarray): matrix of endogenous regressors (features)
            z (np.ndarray): matrix of exogenous regressors (tools)
            y (np.ndarray): matrix a teacher
        """
        x = self._add_bias(x)
        p = z @ np.linalg.inv(z.T @ z) @ z.T
        tmp = np.linalg.inv(x.T @ p @ x) @ x.T @ p @ y
        self._beta = tmp[int(self._fit_bias) :]
        self._bias = tmp[0][0] * int(self._fit_bias)
