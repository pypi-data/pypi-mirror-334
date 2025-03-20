# Third-party libraries
import numpy as np

# First-party libraries
from pamm.algorithms.base_model import AbstractBaseModelAlgorithm


def cv(
    model: AbstractBaseModelAlgorithm, x: np.array, y: np.array, cv: int = 2
) -> None:
    len_ds = int(np.ceil(x.shape[0] / cv))
    models = [model for _ in range(cv)]

    for num, model in enumerate(models):
        x_reduce = x[num * len_ds : (num + 1) * len_ds]
        y_reduce = y[num * len_ds : (num + 1) * len_ds]
        model.fit(x=x_reduce, y=y_reduce)
