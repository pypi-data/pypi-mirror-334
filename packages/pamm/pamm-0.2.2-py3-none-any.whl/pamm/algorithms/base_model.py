# Standard Library
from abc import ABC, abstractmethod


class AbstractBaseModelAlgorithm(ABC):
    @abstractmethod
    def fit(self):
        """Get fitting of model."""

    @abstractmethod
    def predict(self):
        """Get predict of model."""


class AbstractRegressionModelAlgorithm(ABC):
    @property
    @abstractmethod
    def beta(self):
        """Get coefficients of model."""

    @property
    @abstractmethod
    def bias(self):
        """Get bias of model."""


class AbstractTreeModelAlgorithm(ABC):
    """Abstruct for Tree"""


class AbstractNeyroModelAlgorithm(ABC):
    """Abstruct for Neyro"""
