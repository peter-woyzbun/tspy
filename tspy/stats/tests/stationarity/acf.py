import numpy as np

from tspy.time_series import TimeSeries
from tspy.datasets import female_births_ca


class Acf(object):

    def __init__(self, n_lags=None, alpha=None, qstat=False):
        self.n_lags = n_lags
        self.alpha = alpha
        self.qstat = qstat

    def run(self, time_series: TimeSeries):
        x = time_series.x
        n = len(x) if self.n_lags is None else self.n_lags
        variance = x.var()
        x = x - x.mean()
        r = np.correlate(x, x, mode='full')[-n:]
        assert np.allclose(r, np.array([(x[:n - k] * x[-(n - k):]).sum() for k in range(n)]))
        result = r / (variance * (np.arange(n, 0, -1)))
        return result


acf = Acf(n_lags=15)

print(acf.run(time_series=female_births_ca))