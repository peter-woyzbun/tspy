from abc import abstractmethod
import operator

from tspy.time_series import TimeSeries


class PredictiveModel(object):

    def __init__(self, model_name, component_type_name, child_model_types=None):
        self.model_name = model_name
        self.component_type_name = component_type_name
        self.child_model_types = child_model_types
        self.child_model = None
        self.child_composition_op = None
        self.parent_model = None
        self.component_fit_ts = None
        self.training_ts = None

    def copy(self):
        pass

    @property
    @abstractmethod
    def X(self):
        pass

    @property
    def component_residual_ts(self):
        return self.training_ts - self.component_fit_ts

    @property
    def residual_ts(self):
        residuals = self.training_ts
        for model_component in self.components():
            residuals -= model_component.component_fit_ts
        return residuals

    def __add__(self, other):
        if not isinstance(other, PredictiveModel):
            raise TypeError
        elif self.child_model_types is None:
            raise TypeError
        elif type(other) in self.child_model_types:
            self.child_model = other
            self.child_composition_op = operator.add
            other.parent_model = self
            return self
        else:
            raise TypeError

    def components(self):
        current_component = self.root_model()
        while current_component is not None:
            yield current_component
            current_component = current_component.child_model

    def root_model(self):
        if self.parent_model is None:
            return self
        else:
            return self.parent_model.root_model()

    @property
    def is_root_model(self):
        return self.parent_model is None

    def train(self, time_series: TimeSeries):
        """ Only called from root-component... """
        if not self.is_root_model:
            raise Exception
        self.train_component(time_series=time_series)

    def train_component(self, time_series: TimeSeries):
        self._train_component(time_series=time_series)
        self._post_train_checks()
        if self.child_model is not None:
            self.child_model.train_component(time_series=self.component_residual_ts)

    @abstractmethod
    def _train_component(self, time_series: TimeSeries):
        pass

    def _post_train_checks(self):
        assert isinstance(self.component_fit_ts, TimeSeries)

    def _make_fit_ts(self, y_fit):
        component_fit_ts = TimeSeries.from_array(array=y_fit,
                                                 start_date=self.training_ts.start_date,
                                                 freq=self.training_ts.freq,
                                                 var_desc="model fit")
        self.component_fit_ts = component_fit_ts

    def summary(self):
        pass

    def _summary(self):
        pass
