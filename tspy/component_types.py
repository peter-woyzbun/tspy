

class ModelComponentType(object):

    def __init__(self, precedent_types=None, not_composable_with=None, is_singular=True):
        self.precedent_types = precedent_types
        self.not_composable_with = not_composable_with
        self.is_singular = is_singular

    def is_composable_with(self, components):
        for component in components:
            if self.not_composable_with is not None and type(component) in self.not_composable_with:
                return False
            elif self.is_singular and type(self) == type(component):
                return False
        return True

    def takes_precedence_over(self, component):
        if self.precedent_types is None:
            return True
        elif type(component) not in self.precedent_types:
            return True
        else:
            return False


class Trend(ModelComponentType):

    def __init__(self):
        ModelComponentType.__init__(self, precedent_types=None, is_singular=True)


class Cyclical(ModelComponentType):

    def __init__(self):
        ModelComponentType.__init__(self, precedent_types=(Trend,), is_singular=True)


class Seasonal(ModelComponentType):

    def __init__(self, num_harmonics):
        self.num_harmonics = num_harmonics

        ModelComponentType.__init__(self, precedent_types=(Trend, Cyclical), is_singular=False)

    def takes_precedence_over(self, component):
        if type(component) == Seasonal:
            return self.num_harmonics < component.num_harmonics
        else:
            return ModelComponentType.takes_precedence_over(self, component=component)


class Intervention(ModelComponentType):

    def __init__(self):
        ModelComponentType.__init__(self, precedent_types=(Trend, Cyclical, Seasonal), is_singular=False)