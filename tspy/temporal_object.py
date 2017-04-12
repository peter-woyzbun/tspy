import copy

import pandas as pd
import numpy as np

from tspy.exceptions import TimeSeriesException


class TemporalObject(object):

    def __init__(self, series, freq):
        if series is not None and not isinstance(series, pd.Series):
            raise TimeSeriesException
        self.series = series
        self.freq = freq

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

    def get_obs(self, number: int):
        """ Return the observation value for the given index value. """
        return self.series.iloc[number]

    def obs_date(self, obs_num):
        """ Return the datetime for the given observation number. """
        return self.series.index[obs_num]

    def obs_num_from_date(self, date):
        return self.series.get_loc(date)

    def split(self, at_obs: int):
        """ Split the TemporalObject instance at the given observation number. """
        return self[0:at_obs], self[at_obs:]

    def x(self, as_date=False):
        if as_date:
            return self.series.index.values
        else:
            return np.arange(self.n_obs)

    def y(self):
        return self.series.values

    def copy(self):
        return copy.deepcopy(self)

    @property
    def months(self):
        return self.series.index.month

    def month_ends(self):
        months = self.series.index.month
        ends = np.where(months[:-1] != months[1:])[0]
        end_dates = [self.obs_date(i) for i in ends]
        return end_dates

    def month_starts(self):
        starts = [1]
        current_month = self.months[0]
        for obs_num, month_val in enumerate(self.months):
            if month_val != current_month:
                starts.append(obs_num)
                current_month = month_val
        start_dates = [self.obs_date(i) for i in starts]
        return start_dates



