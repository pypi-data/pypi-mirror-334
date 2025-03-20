"""File with cross-validation regression model algorithm."""

# Third-party libraries
import numpy as np

# First-party libraries
from pamm.algorithms.base_model import AbstractRegressionAlgorithm


class CVRegressionAlgorithm(AbstractRegressionAlgorithm):
    def __init__(self, fit_intercept: bool = True) -> None:
        self._fit_intercept = fit_intercept

    def fit(self, x_matrix: np.ndarray, y_vector: np.ndarray, cv: int = 5) -> None:
        """Fit model.

        Args:
            x_matrix (np.ndarray): matrix of regression
            y_vector (np.ndarray): matrix a teacher data
            cv (int): the number of divisions of the dataset
        """

        if self._fit_intercept:
            x_matrix = np.hstack([np.ones((x_matrix.shape[0], 1)), x_matrix])

        len_ds = int(np.ceil(x_matrix.shape[0] / cv))

        b_matrix = np.zeros((len_ds - 1, x_matrix.shape[1]))

        for ds in range(cv):
            x_reduce = x_matrix[ds * len_ds : (ds + 1) * len_ds]
            y_reduce = y_vector[ds * len_ds : (ds + 1) * len_ds]
            beta = np.linalg.inv(x_reduce.T @ x_reduce) @ x_reduce.T @ y_reduce
            b_matrix[ds] = beta.T

        tmp = np.atleast_2d(np.mean(b_matrix, axis=0)).T

        self._beta_coefs = tmp[int(self._fit_intercept) :]
        self._intercept = tmp[0][0] * int(self._fit_intercept)

    def predict(self, x_matrix: np.ndarray) -> np.ndarray:
        """Get predict values.

        Args:
            x_matrix (np.ndarray): matrix of regression

        Returns:
            np.ndarray: Predicted values
        """
        return x_matrix @ self._beta_coefs + self._intercept

    @property
    def beta_coefs(self) -> np.ndarray:
        """Get beta coefficents.

        Returns:
            np.ndarray: vector of beta coefficients.
        """
        return self._beta_coefs

    @beta_coefs.setter
    def beta_coefs(self, new_beta: tuple) -> None:
        """Set beta coefficients in manual mode.

        Args:
            new_beta (tuple): new beta coefficients
        """
        self._beta_coefs = np.atleast_2d(new_beta).T

    @property
    def intercept(self) -> float:
        """Get intercept.

        Returns:
            float: intercept
        """
        return self._intercept

    @intercept.setter
    def intercept(self, intercept: float) -> None:
        """Set intercept a manual mode.

        Args:
            intercept (float): new intercept
        """
        self._intercept = intercept
