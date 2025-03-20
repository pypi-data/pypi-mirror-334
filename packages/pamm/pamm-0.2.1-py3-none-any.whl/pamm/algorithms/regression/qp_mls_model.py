"""File with quad prog algorithm."""

# Third-party libraries
import cvxopt as quad_prog_cvx
import numpy as np

# First-party libraries
from pamm.algorithms.regression.regression_model import RegressionAlgorithm


class QPMLSAlgorithm(RegressionAlgorithm):
    """Class for calculating linear model coefficients using MRLS(weighted Least Squares) + Quadprog."""

    def _add_bias(
        self, x: np.ndarray, min: np.ndarray, max: np.ndarray
    ) -> tuple[np.ndarray]:
        if self._fit_bias:
            return (
                np.hstack([np.ones((x.shape[0], 1)), x]),
                np.vstack([-100000, min]),
                np.vstack([100000, max]),
            )
        return x, min, max

    def fit(
        self,
        x: np.ndarray,
        y: np.ndarray,
        r: np.ndarray,
        q: np.ndarray,
        beta_apriory: np.ndarray,
        beta_min: np.ndarray,
        beta_max: np.ndarray,
    ) -> None:
        """The method of calculating coefficients is the RLS method using quadprog.

        Args:
            x_matrix (np.ndarray): matrix of regressors
            y_vector (np.ndarray): teacher vector
            r_matrix (np.ndarray): data trust matrix
            beta_min (np.atleast_2d): tuple with minimum values of regressors
            beta_max (np.atleast_2d): tuple with maximum values of regressors
        """

        x, beta_min, beta_max = self._add_bias(x, beta_min, beta_max)

        _, count_features = x.shape

        h = 2 * (x.T @ r @ x + q)
        f = (-2 * (y.T @ r @ x + beta_apriory @ q)).T
        a = np.concatenate(
            (np.identity(count_features), -np.identity(count_features)), axis=0
        )
        b = np.concatenate((beta_max, -beta_min), axis=0)

        p = quad_prog_cvx.matrix(h.astype(np.double))
        q = quad_prog_cvx.matrix(f.astype(np.double))
        g = quad_prog_cvx.matrix(a.astype(np.double))
        h = quad_prog_cvx.matrix(b.astype(np.double))

        quad_prog_cvx.solvers.options["kktsolver"] = "ldl"
        quad_prog_cvx.solvers.options["feastol"] = 1e-16
        quad_prog_cvx.solvers.options["maxiters"] = 1000

        res_quadprog = quad_prog_cvx.solvers.qp(P=p, q=q, G=g, h=h)["x"].T
        tmp = np.atleast_2d(res_quadprog)[0].reshape(count_features, 1)

        self._beta = tmp[int(self._fit_bias) :]
        self._bias = tmp[0][0] * int(self._fit_bias)
