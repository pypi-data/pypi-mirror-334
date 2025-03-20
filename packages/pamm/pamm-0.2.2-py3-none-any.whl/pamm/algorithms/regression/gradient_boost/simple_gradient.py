# Third-party libraries
import numpy as np


def bgd(
    x: np.ndarray, y: np.ndarray, eta: float = 0.1, max_iter: int = 1000
) -> np.ndarray:
    m, n = x.shape
    theta = np.random.randn(n, 1)
    for iteration in range(max_iter):
        gradients = 2 / m * x.T @ (x @ theta - y)
        theta = theta - eta * gradients
    return theta


def sgd(
    x: np.ndarray,
    y: np.ndarray,
    eta: float = 0.1,
    n_epochs: int = 10,
    t0: int = 1,
    t1: int = 10,
) -> np.ndarray:
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
    return theta
