from tspy.result_set import ResultSet
from tspy.stats.tests.trend.mann_kendall import MannKendallTest
from tspy.time_series import TimeSeries


class SeasonalMannKendallTest(object):

    def __init__(self, num_seasons):
        self.num_seasons = num_seasons
        self.results = ResultSet(name="Seasonal Mann-Kenall Test")

    def run(self, time_series: TimeSeries):
        seasonal_series = time_series.make_subsets(n_subsets=self.num_seasons)
        for seasons_ts in seasonal_series:
            season_mann_kendall = MannKendallTest()
            season_mann_kendall.run(time_series=seasons_ts)