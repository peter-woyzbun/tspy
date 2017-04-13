import numpy as np
from scipy import stats

from tspy.result_set import ResultSet
from tspy.time_series import TimeSeries


class MannKendallTest(object):
    """

    References
    ----------
    http://vsp.pnnl.gov/help/Vsample/Design_Trend_Mann_Kendall.htm

    """

    def __init__(self):
        self.results = ResultSet(name="Mann-Kendall Test")

    def run(self, time_series: TimeSeries, alpha=0.05):
        y = time_series.y()
        n = len(y)

        # calculate S
        s = 0
        for k in range(n - 1):
            for j in range(k + 1, n):
                s += np.sign(y[j] - y[k])

        # calculate the unique data
        unique_x = np.unique(y)
        g = len(unique_x)

        # calculate the var(s)
        if n == g:  # there is no tie
            var_s = (n * (n - 1) * (2 * n + 5)) / 18
        else:  # there are some ties in data
            tp = np.zeros(unique_x.shape)
            for i in range(len(unique_x)):
                tp[i] = sum(unique_x[i] == y)
            var_s = (n * (n - 1) * (2 * n + 5) + np.sum(tp * (tp - 1) * (2 * tp + 5))) / 18

        if s > 0:
            z = (s - 1) / np.sqrt(var_s)
        elif s == 0:
            z = 0
        elif s < 0:
            z = (s + 1) / np.sqrt(var_s)

        # calculate the p_value
        p = 2 * (1 - stats.norm.cdf(abs(z)))  # two tail test
        h = abs(z) > stats.norm.ppf(1 - alpha / 2)

        if (z < 0) and h:
            trend = 'decreasing'
        elif (z > 0) and h:
            trend = 'increasing'
        else:
            trend = 'no trend'

        self.results.add_results(trend=trend, has_trend=h, p_value=p, z_value=z, S=s, n_obs=n)
