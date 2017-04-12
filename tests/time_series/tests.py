import unittest
import datetime

from tspy.datasets import female_births_ca


class TimeSeriesTests(unittest.TestCase):

    def test_start_date(self):
        expected_dt = datetime.datetime(1959, 1, 1)
        self.assertEquals(expected_dt, female_births_ca.start_date)

    def test_end_date(self):
        expected_dt = datetime.datetime(1959, 12, 31)
        self.assertEquals(expected_dt, female_births_ca.end_date)

    def test_future_dt_index(self):
        future_dt_index = female_births_ca.future_dt_index(n_periods=5)
        expected_dt = datetime.datetime(1960, 1, 1)
        self.assertEquals(future_dt_index.min(), expected_dt)

    def test_get_obs(self):
        self.assertEquals(35, female_births_ca.get_obs(number=0))