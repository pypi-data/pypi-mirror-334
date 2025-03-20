# Third-party libraries
import numpy as np

# First-party libraries
from pamm.algorithms.base_model import AbstractRegressionModelAlgorithm


class RegressionAlgorithm(AbstractRegressionModelAlgorithm):
    def __init__(self, fit_bias: bool = True) -> None:
        self._fit_bias: bool = fit_bias
        self._beta: np.array | None = None
        self._bias: float = 0

    def _add_bias(self, x: np.array) -> np.array:
        if self._fit_bias:
            return np.hstack([np.ones((x.shape[0], 1)), x])
        return x

    def fit(self, x: np.ndarray, y: np.ndarray) -> None:
        """Fit model.
        Args:
            x_matrix (np.ndarray): matrix of regression
            y_vector (np.ndarray): matrix a teacher data
        """
        x = self._add_bias(x)
        tmp = np.linalg.inv(x.T @ x) @ x.T @ y
        self._beta = tmp[int(self._fit_bias) :]
        self._bias = tmp[0][0] * int(self._fit_bias)

    def predict(self, x: np.ndarray) -> np.ndarray:
        """Get predict values.

        Args:
            x_matrix (np.ndarray): matrix of regression

        Returns:
            np.ndarray: Predicted values
        """
        return x @ self._beta + self._bias

    @property
    def beta(self) -> np.ndarray:
        """Get beta coefficents.

        Returns:
            np.ndarray: vector of beta coefficients.
        """
        return self._beta

    @beta.setter
    def beta(self, new_beta: tuple) -> None:
        """Set beta coefficients in manual mode.

        Args:
            new_beta (tuple): new beta coefficients
        """
        self._beta = np.atleast_2d(new_beta).T

    @property
    def bias(self) -> float:
        """Get intercept.

        Returns:
            float: intercept
        """
        return self._bias

    @bias.setter
    def bias(self, num: float) -> None:
        """Set intercept a manual mode.

        Args:
            intercept (float): new intercept
        """
        self._bias = num
