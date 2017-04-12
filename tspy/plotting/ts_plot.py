import matplotlib.pyplot as plt

from tspy.temporal_object import TemporalObject
from tspy.time_series import TimeSeries
from tspy.datasets import female_births_ca


class TimeSeriesPlot(TemporalObject):

    def __init__(self, time_series: TimeSeries):
        TemporalObject.__init__(self, series=time_series.series, freq=time_series.freq)

    def save_plot(self):
        plot = plt.plot(self.x(as_date=True), self.y())
        plt.savefig('test.png')


test_plot = TimeSeriesPlot(time_series=female_births_ca)

test_plot.save_plot()