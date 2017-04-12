import datetime
import copy

import pandas as pd
import numpy as np

from tspy.temporal_object import TemporalObject


class TimeSeries(TemporalObject):

    def __init__(self, series, freq):
        TemporalObject.__init__(self, series=series, freq=freq)

    @classmethod
    def from_array(cls, array, start_date, freq):
        periods = len(array)
        dt_index = pd.date_range(start=start_date, periods=periods, freq=freq)
        ts = pd.Series(array, index=dt_index)
        return TimeSeries(series=ts, freq=freq)

    @classmethod
    def from_dataframe(cls, df, var_name, freq):
        ts = pd.Series(df[var_name].values, index=pd.DatetimeIndex(df['date']))
        return TimeSeries(series=ts, freq=freq)

    @classmethod
    def from_csv(cls, csv_path, var_name, freq, date_fmt):
        df = pd.read_csv(csv_path)
        dates = pd.to_datetime(df['date'], format=date_fmt)
        ts = pd.Series(df[var_name].values, index=pd.DatetimeIndex(dates))
        return TimeSeries(series=ts, freq=freq)

    def moving_avg(self, window):
        new_copy = self.copy()
        new_copy.ts = self.series.rolling(window)
        return new_copy

    def future_dt_index(self, n_periods: int) -> pd.DatetimeIndex:
        """
        Return a pandas DateTimeIndex instance containing n_periods
        of datetimes in the 'future'.

        """
        dt_index = pd.DatetimeIndex(start=self.end_date, periods=n_periods, freq=self.freq)
        dt_index = dt_index.drop([self.end_date])
        return dt_index

    def make_subsets(self, n_subsets: int):
        subsets = list()
        chunk_size = self.n_obs / n_subsets
        for i in range(n_subsets):
            subsets.append(self[i: i + chunk_size])
        return subsets

