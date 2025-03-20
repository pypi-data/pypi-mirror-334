"""File with regression model algorithm on two-stage least sqares."""

# Third-party libraries
import numpy as np

# First-party libraries
from pamm.algorithms.regression.regression_model import RegressionAlgorithm


class JackKnifeRegressionAlgorithm(RegressionAlgorithm):
    def fit(self, x: np.ndarray, y: np.ndarray) -> None:
        """Fit model.

        Args:
            x (np.ndarray): matrix of endogenous regressors (features)
            y (np.ndarray): matrix a teacher
        """
        x = self._add_bias(x)

        betas = np.zeros(x.T.shape)

        for i in range(x.shape[0]):
            x_reduce = np.delete(x, i, axis=0)
            y_reduce = np.delete(y, i, axis=0)
            betas[:, 0] = (
                np.linalg.inv(x_reduce.T @ x_reduce) @ x_reduce.T @ y_reduce
            ).T

        tmp = np.atleast_2d(np.mean(betas, axis=1)).T

        self._beta = tmp[int(self._fit_bias) :]
        self._bias = tmp[0][0] * int(self._fit_bias)
