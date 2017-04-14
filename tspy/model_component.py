from abc import abstractmethod

from tspy.component_types import ModelComponentType


class ModelComponent(object):

    def __init__(self, component_type: ModelComponentType):
        self.component_type = component_type
        self.child = None
        self.parent = None
        self.decomposed_series = None
        self.train_fit = None
        self.is_trained = False

    def __add__(self, other):
        if not isinstance(other, ModelComponent):
            raise TypeError
        if not self.component_type.is_composable_with(list(self.root_component.model_components())):
            raise TypeError
        if not self.component_type.takes_precedence_over(other):
            other.child = self
            self.parent = other
            return other
        else:
            self.child = other
            other.parent = self
            return self

    @property
    def root_component(self):
        if self.parent is None:
            return self
        else:
            return self.parent.root_component

    @property
    def all_components(self):
        return list(self.root_component.descendants())

    def is_root_component(self):
        return self.parent is None

    def model_components(self):
        yield self
        if self.child is not None:
            yield self.child.model_components()

    def descendants(self):
        if self.child is None:
            return None
        else:
            yield self.child
            yield self.child.descendants()

    def train(self, time_series):
        self._train(time_series)
        if self.parent is not None:
            self.parent.train_fit += self.train_fit
        if self.child is not None:
            self.child.train(time_series=self.decomposed_series)

    @abstractmethod
    def _train(self, time_series):
        pass