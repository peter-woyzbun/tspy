from abc import abstractmethod

from tspy.forecast.models.predictive_model import PredictiveModel
from tspy.time_series import TimeSeries
from tspy.forecast.models.intervention.model import InterventionModel
from tspy.forecast.models.residual import Residual


class SeasonalModel(PredictiveModel):

    def __init__(self, model_name):
        PredictiveModel.__init__(self,
                                 component_type_name='seasonal',
                                 model_name=model_name,
                                 child_model_types=(InterventionModel, Residual))

    @abstractmethod
    def _train_component(self, time_series: TimeSeries):
        pass