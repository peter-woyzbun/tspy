import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt

from tspy.time_series import TimeSeries
from tspy.result_set import ResultSet
from tspy.datasets import female_births_ca
from tspy.utils.stats import significance_code
from tspy.forecast.models.trend.model import TrendModel


class LinearTrend(TrendModel):

    def __init__(self):
        TrendModel.__init__(self, model_name="Linear Trend")

    @property
    def X(self):
        x = self.training_ts.x
        ones = np.ones(len(x))
        return np.concatenate(([ones], [x])).T

    def _train_component(self, time_series: TimeSeries):
        self.training_ts = time_series
        coefficients = self.fit(X=self.X, y=self.training_ts.y)
        y_fit = self._make_fit_values(coefficients=coefficients)
        self._make_fit_ts(y_fit=y_fit)
        t_values, p_values = self._calculate_coeff_stats(coefficients=coefficients)

    @staticmethod
    def fit(X, y):
        U, S, V = np.linalg.svd(X.T.dot(X))
        S = np.diag(S)
        x_sq_inv = V.dot(np.linalg.pinv(S)).dot(U.T)
        coefficients = x_sq_inv.dot(X.T).dot(y)
        return coefficients

    def _make_fit_values(self, coefficients):
        X = self.X
        y_fit = X.dot(coefficients)
        return y_fit

    def _calculate_coeff_stats(self, coefficients):
        X = self.X
        sse = np.sum((np.subtract(self.component_fit_ts.y, self.training_ts.y)) ** 2, axis=0) / float(X.shape[0] - X.shape[1])
        se = np.array(np.sqrt(np.diagonal(sse * np.linalg.inv(np.dot(X.T, X)))))
        t_values = coefficients / se
        p_values = 2 * (1 - stats.t.cdf(np.abs(t_values), self.training_ts.y.shape[0] - X.shape[1]))
        return t_values, p_values


class LinearTrendOld(object):

    # Todo: residuals, summary, summary format, clean-up.

    def __init__(self):
        self.time_series = None
        self.train_fit = ResultSet(name="Training")
        self.test_fit = ResultSet(name="Test")
        self.X = None

    def train(self, time_series: TimeSeries):
        self.time_series = time_series
        self._make_X(x=time_series.x())
        coefficients = self.fit(X=self.X, y=time_series.y())
        self._make_fit_values(coefficients=coefficients)
        t_values, p_values = self._calculate_coeff_stats(coefficients=coefficients)
        self._set_train_results(coefficients=coefficients, t_values=t_values, p_values=p_values)

    def _set_train_results(self, coefficients, t_values, p_values):
        self.train_fit.add_summary_results(n_obs=self.time_series.n_obs,
                                           start_date=self.time_series.start_date,
                                           end_date=self.time_series.end_date,
                                           constant=coefficients[0],
                                           slope=coefficients[1])
        self.train_fit.add_table_results(table_name="Coefficients",
                                         coefficient='constant',
                                         estimate=coefficients[0],
                                         t_value=t_values[0],
                                         p_value=p_values[0],
                                         significance=significance_code(p_values[1]))
        self.train_fit.add_table_results(table_name="Coefficients",
                                         coefficient='x',
                                         estimate=coefficients[1],
                                         t_value=t_values[1],
                                         p_value=p_values[1],
                                         significance=significance_code(p_values[0]))

    def _make_fit_values(self, coefficients):
        X = self.X
        print(X)
        y_pred = X.dot(coefficients)
        dt_index = self.time_series.dt_index
        self.series = pd.Series(y_pred, index=dt_index)

    def _calculate_coeff_stats(self, coefficients):
        X = self.X
        sse = np.sum((np.subtract(self.y(), self.time_series.y())) ** 2, axis=0) / float(X.shape[0] - X.shape[1])
        se = np.array(np.sqrt(np.diagonal(sse * np.linalg.inv(np.dot(X.T, X)))))
        t_values = coefficients / se
        p_values = 2 * (1 - stats.t.cdf(np.abs(t_values), self.time_series.y().shape[0] - X.shape[1]))
        return t_values, p_values

    def fit_ts(self, time_series: TimeSeries):
        pass

    def _make_X(self, x):
        ones = np.ones(len(x))
        self.X = np.concatenate(([ones], [x])).T

    @staticmethod
    def fit(X, y):
        U, S, V = np.linalg.svd(X.T.dot(X))
        S = np.diag(S)
        x_sq_inv = V.dot(np.linalg.pinv(S)).dot(U.T)
        coefficients = x_sq_inv.dot(X.T).dot(y)
        return coefficients

    def plot(self):
        plt.plot(self.time_series.x(as_date=True), self.time_series.y(), color='k')
        plt.plot(self.time_series.x(as_date=True), self.y(), color='g')
        plt.xlabel('Date')
        plt.ylabel(self.time_series.var_desc)
        plt.savefig('test.png')


# lin_trend = LinearTrend()
# lin_trend.train(time_series=female_births_ca)
# lin_trend.train_fit.summary()
# lin_trend.plot()