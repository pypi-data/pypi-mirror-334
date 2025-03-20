# First-party libraries
from pamm.algorithms.regression.gradient_boost.pgd_regression import \
    BatchGradientRegressionAlgorithm
from pamm.algorithms.regression.gradient_boost.sgd_regression import \
    StachosticGradientRegressionAlgorithm
from pamm.algorithms.regression.iterations_regression import \
    IterationRegressionAlgorithm
from pamm.algorithms.regression.jackknife_model import \
    JackKnifeRegressionAlgorithm
from pamm.algorithms.regression.qp_mls_model import QPMLSAlgorithm
from pamm.algorithms.regression.regression_model import RegressionAlgorithm
from pamm.algorithms.regression.regularization.elastic_net import \
    ElasticNetRegressionAlgorithm
from pamm.algorithms.regression.regularization.lasso_model import \
    LassoRegressionAlgorithm
from pamm.algorithms.regression.regularization.ridge_model import \
    RidgeRegressionAlgorithm
from pamm.algorithms.regression.tsls_model import TwoStageLeastSquaresAlgorithm
from pamm.algorithms.regression.wls.mls_model import ModifyRegressionAlgorithm
from pamm.algorithms.regression.wls.qp_model import QPRegressionAlgorithm
from pamm.algorithms.regression.wls.wls_model import \
    WeigthedRegressionAlgorithm
from pamm.algorithms.regression.wls.wtsls_model import \
    WeightedTwoStageLeastSquaresAlgorithm
