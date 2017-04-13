import numpy as np
from scipy import stats
import pandas as pd


class RegressionMixin(object):

    @staticmethod
    def linear_fit(X, y):
        U, S, V = np.linalg.svd(X.T.dot(X))
        S = np.diag(S)
        x_sq_inv = V.dot(np.linalg.pinv(S)).dot(U.T)
        coefficients = x_sq_inv.dot(X.T).dot(y)
        return coefficients

    @staticmethod
    def coefficient_stats(coefficients, X, predicted_y, actual_y):
        sse = np.sum((np.subtract(predicted_y, actual_y)) ** 2, axis=0) / float(X.shape[0] - X.shape[1])
        se = np.array(np.sqrt(np.diagonal(sse * np.linalg.inv(np.dot(X.T, X)))))
        t_values = coefficients / se
        p_values = 2 * (1 - stats.t.cdf(np.abs(t_values), actual_y.shape[0] - X.shape[1]))
        return t_values, p_values

    @staticmethod
    def make_fit_values(X, time_series, coefficients):
        y_pred = X.dot(coefficients)
        dt_index = time_series.dt_index
        return pd.Series(y_pred, index=dt_index)