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
        self.assertEquals(35, female_births_ca.get_obs_num(number=0))

    def test_get_obs_num_dt(self):
        self.assertEquals(datetime.datetime(1959, 1, 1), female_births_ca.get_obs_num_dt(0))

    def test_month_starts(self):
        test_ts = female_births_ca[0:62]
        expected_starts = {datetime.datetime(1959, 1, 1, 0, 0, 0),
                           datetime.datetime(1959, 2, 1, 0, 0, 0),
                           datetime.datetime(1959, 3, 1, 0, 0, 0)}
        self.assertEquals(expected_starts, set(test_ts.month_starts()))