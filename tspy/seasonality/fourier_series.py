from tspy.component_types import Seasonal
from tspy.model_component import ModelComponent


class SeasonalFourier(ModelComponent):

    def __init__(self, period, num_harmonics):
        self.period = period
        self.num_harmonics = num_harmonics

        ModelComponent.__init__(self, component_type=Seasonal())

    def _train(self, time_series):
        pass

