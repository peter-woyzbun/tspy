import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

from tspy.time_series import TimeSeries
from tspy.datasets import female_births_ca


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


class PolynomialTrend(RegressionMixin):

    def __init__(self, degree=2):
        self.time_series = None
        self.degree = degree
        self.X = None

    def train(self, time_series: TimeSeries):
        self.time_series = time_series
        self._make_X(x=time_series.x())
        X = self.X
        y = self.time_series.y()
        coefficients = np.dot(np.dot(np.linalg.inv(np.dot(X.T, X)), X.T), y)
        print(coefficients)
        self.series = self.make_fit_values(X=self.X, coefficients=coefficients, time_series=time_series)

    def _make_X(self, x):
        df = pd.DataFrame({'x_0': [1] * len(x)})
        for i in range(1, self.degree + 1):
            df['x_%s' % i] = np.power(x, float(i))
        self.X = df.as_matrix()

    def plot(self):
        plt.plot(self.time_series.x(as_date=True), self.time_series.y(), color='k')
        plt.plot(self.time_series.x(as_date=True), self.y(), color='g')
        plt.xlabel('Date')
        plt.ylabel(self.time_series.var_desc)
        plt.savefig('test.png')


poly = PolynomialTrend(degree=6)

poly.train(time_series=female_births_ca)
poly.plot()