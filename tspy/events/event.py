import datetime

import pandas as pd

from tspy.frequency import Frequency, Day


class Event(object):

    def __init__(self, date_time, name, freq: Frequency, pre_periods=0, post_periods=0):
        self.date_time = date_time
        self.name = name
        self.freq = freq
        self.pre_periods = pre_periods
        self.post_periods = post_periods
        self.series = None
        self._make_series()

    def _make_series(self):
        total_periods = 1 + self.pre_periods + self.post_periods
        start_date = self.freq.decrement_datetime(dt=self.date_time, num_periods=self.pre_periods)
        dt_index = pd.date_range(start=start_date, periods=total_periods, freq=self.freq.pandas_alias)
        series = pd.Series([1]*total_periods, index=dt_index)
        self.series = series


test_event = Event(date_time=datetime.datetime(2017, 4, 13), name='Test Event',
                   freq=Day(), pre_periods=3, post_periods=2)

print(test_event.series)




