import matplotlib.pyplot as plt

from tspy.datasets import female_births_ca
from tspy.trend.models.linear import LinearTrend


class TimeSeriesPlot(object):

    def __init__(self, time_series, title, dt_label_fmt=None, x_label=None, y_label=None):
        self.time_series = time_series
        self.title = title
        self.dt_label_fmt = dt_label_fmt
        self.x_label = x_label
        self.y_label = y_label
        self._sub_plots = [self]
        self._overlays = list()

    @property
    def sub_plots(self):
        return plt.subplots()

    @property
    def num_subplots(self):
        return len(self._sub_plots)

    def add_plot_below(self, time_series_plot, share_y_axis=True):
        self._sub_plots.append(time_series_plot)

    def add_vspan(self, ax, start, end, colour, alpha=0.5):
        ax.axvspan(start, end, color=colour, alpha=alpha)

    def add_hline(self, ax, position, line_style, line_width, colour):
        ax.axhline(position, color=colour, linestyle=line_style, linewidth=line_width)

    def add_hspan(self, ax):
        pass

    def set_title(self, ax, text):
        ax.set_title(text)

    def set_x_label(self, ax, text, fontsize):
        pass

    def set_y_label(self, ax, text, fontsize):
        pass

    def overlay_ts(self, time_series, line_style=None, line_width=None, line_colour=None):
        self._overlays.append({'x': time_series.x_datetimes, 'y': time_series.y, 'linecolor': line_colour})

    def add_event(self, event, facecolor=None, alpha=0.5, include_pre=True, include_post=True):
        pass

    def plot(self):
        fig, ax = self.sub_plots
        ax.plot(self.time_series.x_datetimes, self.time_series.y)
        for overlay in self._overlays:
            ax.plot(overlay['x'], overlay['y'])
        plt.savefig('test.png')



test_plot = TimeSeriesPlot(time_series=female_births_ca, title='whatever!')

trend = LinearTrend()
trend.train(time_series=female_births_ca)

test_plot.overlay_ts(time_series=trend.component_fit_ts, line_colour='b')
test_plot.plot()
