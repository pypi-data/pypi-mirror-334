"""File with regression model algorithm on two-stage least sqares."""

# Third-party libraries
import numpy as np

# First-party libraries
from pamm.algorithms.regression.regression_model import RegressionAlgorithm


class StachosticGradientRegressionAlgorithm(RegressionAlgorithm):
    def fit(
        self,
        x: np.ndarray,
        y: np.ndarray,
        eta: float = 0.1,
        n_epochs: int = 10,
        t0: int = 1,
        t1: int = 10,
    ) -> np.ndarray:
        x = self._add_bias(x)
        m, n = x.shape
        theta = np.random.randn(n, 1)
        for epoch in range(n_epochs):
            for i in range(m):
                random_index = np.random.randint(m)
                xi = x[random_index : random_index + 1]
                yi = y[random_index : random_index + 1]
                gradients = 2 * xi.T @ (xi @ theta - yi)
                eta = t0 / ((epoch * m + i) + t1)
                theta = theta - eta * gradients

        self._beta = theta[int(self._fit_bias) :]
        self._bias = theta[0][0] * int(self._fit_bias)
