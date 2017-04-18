from abc import abstractmethod
import operator


class PredictiveModel(object):

    def __init__(self, child_model_types=None):
        self.child_model_types = child_model_types
        self.child_model = None
        self.child_composition_op = None
        self.parent_model = None
        self.component_residual_ts = None
        self.component_fit_ts = None
        self.train_ts = None

    @property
    def residual_ts(self):
        residuals = self.train_ts
        for model_component in self.components():
            residuals -= model_component.component_fit_ts
        return residuals

    def __add__(self, other):
        if self.child_model_types is None:
            raise TypeError
        elif other in self.child_model_types:
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

    def train(self, time_series):
        pass

    @abstractmethod
    def _train(self, time_series):
        pass

    @abstractmethod
    def _train_component(self, time_series):
        pass

