import numpy as np

from tspy.time_series import TimeSeries
from tspy.datasets import female_births_ca


class LinearRegression(object):

    def __init__(self):
        self.model_type = "Linear Regression"
        self.ts = None
        self.coefficients = None
        self.predicted_vals = None
        self.fit_series = None
        self.r2 = None
        self.adj_r2 = None
        self.f_stat = None
        self.log_likelihood = None
        self.aic = None
        self.bic = None

    def fit_ts(self, ts: TimeSeries):
        self.ts = ts
        x = ts.x()
        y = ts.y()
        self.fit(x=x, y=y)

    def fit(self, x, y):
        ones = np.ones(len(x))
        x = np.concatenate(([x], [ones])).T
        print(x)
        # x = np.insert(x, 0, 1, axis=1)
        U, S, V = np.linalg.svd(x.T.dot(x))
        S = np.diag(S)
        x_sq_inv = V.dot(np.linalg.pinv(S)).dot(U.T)
        self.coefficients = x_sq_inv.dot(x.T).dot(y)
        self._calculate_fit_values(x)

    def _calculate_fit_values(self, x):
        y_pred = x.dot(self.coefficients)
        self.fit_series = y_pred


lin_reg = LinearRegression()
lin_reg.fit_ts(female_births_ca)

print(lin_reg.coefficients)