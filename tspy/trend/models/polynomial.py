import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from tspy.temporal_object import TemporalObject
from tspy.time_series import TimeSeries
from tspy.datasets import female_births_ca
from tspy.mixins.regression import RegressionMixin


class PolynomialTrend(TemporalObject, RegressionMixin):

    def __init__(self, degree=2):
        self.time_series = None
        self.degree = degree
        self.X = None
        TemporalObject.__init__(self, series=None, freq=None)

    def train(self, time_series: TimeSeries):
        self.time_series = time_series
        self._make_X(x=time_series.x())
        print(self.X)
        coefficients = self.linear_fit(X=self.X, y=time_series.y())
        print(coefficients)
        self.series = self.make_fit_values(X=self.X, coefficients=coefficients, time_series=time_series)

    def _make_X(self, x):
        df = pd.DataFrame({'x_0': [1] * len(x)})
        for i in range(1, self.degree + 1):
            df['x_%s' % i] = x ** i
        self.X = df.as_matrix()

    def plot(self):
        plt.plot(self.time_series.x(as_date=True), self.time_series.y(), color='k')
        plt.plot(self.time_series.x(as_date=True), self.y(), color='g')
        plt.xlabel('Date')
        plt.ylabel(self.time_series.var_desc)
        plt.savefig('test.png')


poly = PolynomialTrend(degree=3)

poly.train(time_series=female_births_ca)
poly.plot()