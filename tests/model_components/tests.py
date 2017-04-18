import unittest
import datetime

from numpy import testing as np_testing

from tspy.residual import Residual
from tspy.trend.models.linear import LinearTrend
from tspy.time_series import TimeSeries
from tspy.frequency import Day


class ResidualTests(unittest.TestCase):

    test_ts = TimeSeries.zeroes(start_date=datetime.datetime(2017, 1, 1), freq=Day(), periods=30)

    def test_residual_component_ts(self):
        residual = Residual()
        residual.train_component(time_series=self.test_ts)
        np_testing.assert_array_equal(self.test_ts.y, residual.component_fit_ts.y)

    def test_residual_residual_ts(self):
        residual = Residual()
        residual.train_component(time_series=self.test_ts)
        np_testing.assert_array_equal(self.test_ts.y, residual.component_residual_ts.y)


class LinearTrendResidualTests(unittest.TestCase):

    test_ts = TimeSeries.random_linear(start_date=datetime.datetime(2017, 1, 1), freq=Day(),
                                       periods=30, mu=0, sigma=0.1)

    def test_trend_residual(self):
        trend = LinearTrend()
        residual = Residual()
        model = trend + residual
        model.train(time_series=self.test_ts)
        self.assertAlmostEquals(0, residual.component_fit_ts.mean())