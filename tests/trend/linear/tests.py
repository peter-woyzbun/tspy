import unittest
import datetime

import numpy as np

from tspy.time_series import TimeSeries
from tspy.forecast.models.trend.models.linear import LinearTrend


class TestLinearTrend(unittest.TestCase):

    def test_constant(self):
        test_ts = TimeSeries.random_linear(start_date=datetime.datetime(2017, 1, 1), periods=100, freq='D', mu=0,
                                           sigma=0.1)
        lin_trend = LinearTrend()
        lin_trend.train(test_ts)
        lin_trend.train_fit.summary()
        self.assertAlmostEqual(lin_trend.train_fit.constant, 0, places=1)

    def test_slope(self):
        test_ts = TimeSeries.random_linear(start_date=datetime.datetime(2017, 1, 1), periods=100, freq='D', mu=0,
                                           sigma=0.1)
        lin_trend = LinearTrend()
        lin_trend.train(test_ts)
        self.assertAlmostEqual(lin_trend.train_fit.slope, 1, places=1)