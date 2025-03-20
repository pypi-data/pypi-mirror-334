"""File with ridge regression model algorithm."""

# Third-party libraries
import numpy as np

# First-party libraries
from pamm.algorithms.regression.regression_model import RegressionAlgorithm


class ElasticNetRegressionAlgorithm(RegressionAlgorithm):
    def fit(
        self,
        x: np.ndarray,
        y: np.ndarray,
        alpha: float = 0.01,
        ratio: float = 0.5,
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
                gradients = (
                    2 * xi.T @ (xi @ b - yi)
                    + ratio * alpha * sum(abs(b))[0]
                    + (1 - ratio) / 2 * alpha * (b.T @ b)[0, 0]
                )
                eta = t0 / ((epoch * m + i) + t1)
                b = b - eta * gradients

        self._beta = b[int(self._fit_bias) :]
        self._bias = b[0][0] * int(self._fit_bias)
