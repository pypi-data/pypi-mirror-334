"""File with laso regression model algorithm."""

# Third-party libraries
import numpy as np

# First-party libraries
from pamm.algorithms.regression.regression_model import RegressionAlgorithm


class LassoRegressionAlgorithm(RegressionAlgorithm):
    def _sign(self, num: float) -> float:
        if num == 0:
            return num
        if num > 0:
            return 1
        if num < 0:
            return -1

    def _sign_vectorize(self, b: np.ndarray) -> np.ndarray:
        vector = np.zeros(b.shape)
        for x in range(b.shape[0]):
            vector[x, 0] = self._sign(b[x, 0])
        return vector

    def fit(
        self,
        x: np.ndarray,
        y: np.ndarray,
        alpha: float = 0.01,
        eta: float = 0.1,
        n_epochs: int = 10,
        t0: int = 1,
        t1: int = 10,
    ) -> np.ndarray:
        x = self._add_bias(x)
        m, n = x.shape
        b = np.random.randn(n, 1)
        for epoch in range(n_epochs):
            for i in range(m):
                random_index = np.random.randint(m)
                xi = x[random_index : random_index + 1]
                yi = y[random_index : random_index + 1]
                gradients = 2 * xi.T @ (xi @ b - yi) + alpha * self._sign_vectorize(b)
                eta = t0 / ((epoch * m + i) + t1)
                b = b - eta * gradients

        self._beta = b[int(self._fit_bias) :]
        self._bias = b[0][0] * int(self._fit_bias)
