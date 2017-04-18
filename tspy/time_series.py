import datetime
import copy

import pandas as pd
import numpy as np

from tspy.temporal_object import TemporalObject
from tspy.frequency import Frequency


class ConstructorMixin(object):

    @classmethod
    def from_array(cls, array, start_date, freq, var_desc):
        periods = len(array)
        dt_index = pd.date_range(start=start_date, periods=periods, freq=freq)
        ts = pd.Series(array, index=dt_index)
        return TimeSeries(series=ts, freq=freq, var_desc=var_desc)

    @classmethod
    def from_dataframe(cls, df, var_name, freq, var_desc):
        ts = pd.Series(df[var_name].values, index=pd.DatetimeIndex(df['date']))
        return TimeSeries(series=ts, freq=freq, var_desc=var_desc)

    @classmethod
    def from_csv(cls, csv_path, var_name, freq, date_fmt, var_desc):
        df = pd.read_csv(csv_path)
        dates = pd.to_datetime(df['date'], format=date_fmt)
        ts = pd.Series(df[var_name].values, index=pd.DatetimeIndex(dates))
        return TimeSeries(series=ts, freq=freq, var_desc=var_desc)

    @classmethod
    def from_json(cls, dt_label, freq, json_data, var_label, dt_fmt, var_desc=None):
        pass

    @classmethod
    def random_linear(cls, start_date, freq, periods, mu, sigma):
        rand_array = np.linspace(0, periods, num=periods, endpoint=False) + np.random.normal(mu, sigma, 100)
        dt_index = pd.date_range(start=start_date, periods=periods, freq=freq)
        series = pd.Series(rand_array, index=dt_index)
        return TimeSeries(series=series, freq=freq, var_desc='Random Linear')


class TimeSeries(object, ConstructorMixin):

    def __init__(self, series: pd.Series, freq: Frequency, var_desc=None):
        self.series = series
        self.freq = freq
        self.var_desc = var_desc

    @property
    def y(self):
        return self.series.values

    @property
    def x(self):
        return np.arange(self.n_obs)

    @property
    def x_datetimes(self):
        return self.series.index.values

    def future_x(self, n_periods):
        return list(range(self.n_obs, self.n_obs + n_periods))

    def future_datetimes(self, n_periods):
        pass

    def df(self):
        return self.series.to_frame()

    def json(self):
        return self.series.to_json()

    def __getitem__(self, item):
        sliced_instance = copy.deepcopy(self)
        sliced_instance.series = sliced_instance.series[item]
        return sliced_instance

    def __iter__(self):
        for x in self.series.values:
            yield x

    def iteritems(self):
        return self.series.iteritems()

    @property
    def dt_index(self) -> pd.DatetimeIndex:
        return self.series.index

    @property
    def start_date(self):
        return self.series.index.min()

    @property
    def end_date(self):
        return self.series.index.max()

    @property
    def n_obs(self):
        return self.series.count()

    def get_obs_num(self, number: int):
        """ Return the observation value for the given index value. """
        return self.series.iloc[number]

    def get_obs_num_dt(self, obs_num):
        """ Return the datetime for the given observation number. """
        return self.series.index[obs_num]

    def split(self, at_obs: int):
        """ Split the TemporalObject instance at the given observation number. """
        return self[0:at_obs], self[at_obs:]

    def copy(self):
        return copy.deepcopy(self)

    @property
    def months(self):
        """
        Return a numpy array indicating the month (i.e 1,...,12) of
        each observation.

        """
        return self.series.index.month

    def month_ends(self):
        """
        Return a list containing the datetime of the end of every month
        contained in this instance.

        """
        months = self.series.index.month
        ends = np.where(months[:-1] != months[1:])[0]
        end_dates = [self.get_obs_num_dt(i) for i in ends]
        return end_dates

    def month_starts(self):
        """
        Return a list containing the datetime of the start of every month
        contained in this instance.

        """
        starts = [1]
        current_month = self.months[0]
        for obs_num, month_val in enumerate(self.months):
            if month_val != current_month:
                starts.append(obs_num)
                current_month = month_val
        start_dates = [self.get_obs_num_dt(i) for i in starts]
        return start_dates

    @property
    def weeks(self):
        return self.series.dt.week

    def week_starts(self):
        starts = [1]
        current_week = self.weeks[0]
        for obs_num, week_val in enumerate(self.weeks):
            if week_val != current_week:
                starts.append(obs_num)
                current_week = week_val
        start_dates = [self.get_obs_num_dt(i) for i in starts]
        return start_dates

    def week_ends(self):
        weeks = self.weeks
        ends = np.where(weeks[:-1] != weeks[1:])[0]
        end_dates = [self.get_obs_num_dt(i) for i in ends]
        return end_dates

    @property
    def day_of_week(self):
        return self.series.dt.dayofweek

    @property
    def years(self):
        return self.series.dt.year

    def year_ends(self):
        """
        Return a list containing the datetime of the end of every year
        contained in this instance.

        """
        years = self.years
        ends = np.where(years[:-1] != years[1:])[0]
        end_dates = [self.get_obs_num_dt(i) for i in ends]
        return end_dates

    def year_starts(self):
        """
        Return a list containing the datetime of the end of every year
        contained in this instance.

        """
        starts = [1]
        current_year = self.years[0]
        for obs_num, year_val in enumerate(self.years):
            if year_val != current_year:
                starts.append(obs_num)
                current_year = year_val
        start_dates = [self.get_obs_num_dt(i) for i in starts]
        return start_dates

    def weekday_nums(self):
        pass

    def day_names(self):
        pass

    def make_subsets(self, n_subsets):
        pass




class TimeSeriesOld(TemporalObject):

    def __init__(self, series, freq, var_desc):
        self.var_desc = var_desc
        TemporalObject.__init__(self, series=series, freq=freq)

    @classmethod
    def from_array(cls, array, start_date, freq, var_desc):
        periods = len(array)
        dt_index = pd.date_range(start=start_date, periods=periods, freq=freq)
        ts = pd.Series(array, index=dt_index)
        return TimeSeries(series=ts, freq=freq, var_desc=var_desc)

    @classmethod
    def from_dataframe(cls, df, var_name, freq, var_desc):
        ts = pd.Series(df[var_name].values, index=pd.DatetimeIndex(df['date']))
        return TimeSeries(series=ts, freq=freq, var_desc=var_desc)

    @classmethod
    def from_csv(cls, csv_path, var_name, freq, date_fmt, var_desc):
        df = pd.read_csv(csv_path)
        dates = pd.to_datetime(df['date'], format=date_fmt)
        ts = pd.Series(df[var_name].values, index=pd.DatetimeIndex(dates))
        return TimeSeries(series=ts, freq=freq, var_desc=var_desc)

    @classmethod
    def random_linear(cls, start_date, freq, periods, mu, sigma):
        rand_array = np.linspace(0, periods, num=periods, endpoint=False) + np.random.normal(mu, sigma, 100)
        dt_index = pd.date_range(start=start_date, periods=periods, freq=freq)
        series = pd.Series(rand_array, index=dt_index)
        return TimeSeries(series=series, freq=freq, var_desc='Random Linear')

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

