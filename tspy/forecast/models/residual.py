from tspy.forecast.models.predictive_model import PredictiveModel
from tspy.time_series import TimeSeries


class Residual(PredictiveModel):

    def __init__(self):
        PredictiveModel.__init__(self,
                                 component_type_name='residual',
                                 model_name='residual')

    def _train_component(self, time_series: TimeSeries):
        self.training_ts = time_series
        self.component_fit_ts = time_series

    @property
    def component_residual_ts(self):
        return self.training_ts

    @property
    def X(self):
        return None


