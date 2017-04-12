from abc import abstractmethod

from tspy.temporal_object import TemporalObject
from tspy.time_series import TimeSeries
from tspy.result_set import ResultSet


class Model(TemporalObject):

    def __init__(self, type_name):
        self.type_name = type_name
        self.train_results = ResultSet(name="Training")
        self.test_results = ResultSet(name="Test")
        self.rolling_test_results = ResultSet(name="Rolling Test")
        TemporalObject.__init__(self, series=None, freq=None)

    @abstractmethod
    def train(self, time_series: TimeSeries):
        pass

    @abstractmethod
    def test(self, time_series: TimeSeries):
        pass

    @abstractmethod
    def rolling_test(self, time_series: TimeSeries):
        pass

    @abstractmethod
    def fitted_ts(self):
        pass

    @abstractmethod
    def forecast(self, n_periods):
        pass