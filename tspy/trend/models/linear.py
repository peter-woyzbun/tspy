import numpy as np
import pandas as pd
from scipy import stats

from tspy.temporal_object import TemporalObject
from tspy.time_series import TimeSeries
from tspy.result_set import ResultSet
from tspy.datasets import female_births_ca


class LinearTrend(TemporalObject):

    def __init__(self):
        self.time_series = None
        self.train_fit = ResultSet(name="Training")
        self.test_fit = ResultSet(name="Test")
        self.X = None
        TemporalObject.__init__(self, series=None, freq=None)

    def train(self, time_series: TimeSeries):
        self.time_series = time_series
        self._make_X(x=time_series.x())
        coefficients = self.fit(X=self.X, y=time_series.y())
        self._make_fit_values(time_series=time_series, coefficients=coefficients)
        t_values, p_values = self._calculate_coeff_stats(time_series=time_series, coefficients=coefficients)
        self._set_train_results(coefficients=coefficients, t_values=t_values, p_values=p_values)

    def _set_train_results(self, coefficients, t_values, p_values):
        self.train_fit.add_results(slope=coefficients[1],
                                   n_obs=self.time_series.n_obs,
                                   start_date=self.time_series.start_date,
                                   end_date=self.time_series.end_date)
        self.train_fit.add_result_row(coefficient='constant',
                                      estimate=coefficients[1],
                                      t_value=t_values[1],
                                      p_value=p_values[1])
        self.train_fit.add_result_row(coefficient='x_1',
                                      estimate=coefficients[0],
                                      t_value=t_values[0],
                                      p_value=p_values[0])

    def _make_fit_values(self, time_series: TimeSeries, coefficients):
        X = self.X
        y_pred = X.dot(coefficients)
        dt_index = time_series.dt_index
        self.series = pd.Series(y_pred, index=dt_index)

    def _calculate_coeff_stats(self, time_series: TimeSeries, coefficients):
        X = self.X
        sse = np.sum((np.subtract(self.y(), time_series.y())) ** 2, axis=0) / float(X.shape[0] - X.shape[1])
        print(sse)
        se = np.array(np.sqrt(np.diagonal(sse * np.linalg.inv(np.dot(X.T, X)))))
        print(se)
        print(coefficients)
        t_values = coefficients / se
        p_values = 2 * (1 - stats.t.cdf(np.abs(t_values), time_series.y().shape[0] - X.shape[1]))
        return t_values, p_values

    def fit_ts(self, time_series: TimeSeries):
        pass

    def _make_X(self, x):
        ones = np.ones(len(x))
        self.X = np.concatenate(([x], [ones])).T

    @staticmethod
    def fit(X, y):
        U, S, V = np.linalg.svd(X.T.dot(X))
        S = np.diag(S)
        x_sq_inv = V.dot(np.linalg.pinv(S)).dot(U.T)
        coefficients = x_sq_inv.dot(X.T).dot(y)
        return coefficients


lin_trend = LinearTrend()
print(female_births_ca.month_starts())
lin_trend.train(time_series=female_births_ca)
lin_trend.train_fit.summary()