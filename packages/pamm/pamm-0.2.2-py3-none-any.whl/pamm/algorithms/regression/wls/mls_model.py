"""File with weigthed regression model algorithm."""

# Third-party libraries
import numpy as np

# First-party libraries
from pamm.algorithms.regression.regression_model import RegressionAlgorithm


class ModifyRegressionAlgorithm(RegressionAlgorithm):
    def _add_bias(
        self, x: np.ndarray, q: np.ndarray, b_apr: np.ndarray
    ) -> tuple[np.ndarray]:
        if self._fit_bias:
            return (
                np.hstack([np.ones((x.shape[0], 1)), x]),
                np.diag(np.hstack([0, np.diag(q)])),
                np.vstack([0, b_apr]),
            )
        return x, q, b_apr

    def fit(
        self,
        x: np.ndarray,
        y: np.ndarray,
        w: np.ndarray,
        q: np.ndarray,
        b_apr: np.ndarray,
    ) -> None:
        """Fit model.

        Args:
            x (np.ndarray): matrix of regressors
            y (np.ndarray): matrix a teacher
            w (np.ndarray): matrix of weights for data
            q (np.ndarray): matrix of weights for beta
            b_apr (np.ndarray): knowns beta coefficients
        """

        x, q, b_apr = self._add_bias(x, q, b_apr)
        tmp = b_apr + (np.linalg.inv(q + x.T @ w @ x) @ x.T @ w) @ (y - x @ b_apr)
        self._beta = tmp[int(self._fit_bias) :]
        self._bias = tmp[0][0] * int(self._fit_bias)
