import datetime


class Frequency(object):

    def __init__(self, pandas_alias, friendly_name, timedelta_key=None):
        self.pandas_alias = pandas_alias
        self.friendly_name = friendly_name
        self.timedelta_key = timedelta_key

    def __str__(self):
        return self.pandas_alias

    def decrement_datetime(self, dt, num_periods):
        if self.timedelta_key is not None:
            return dt - datetime.timedelta(**{self.timedelta_key: num_periods})
        else:
            raise NotImplementedError

    def increment_datetime(self, dt, num_periods):
        if self.timedelta_key is not None:
            return dt + datetime.timedelta(**{self.timedelta_key: num_periods})
        else:
            raise NotImplementedError


class BusinessDay(Frequency):

    def __init__(self):
        Frequency.__init__(self, pandas_alias='B',
                           friendly_name='Business day')


class Day(Frequency):
    def __init__(self):
        Frequency.__init__(self, pandas_alias='D',
                           friendly_name='Day',
                           timedelta_key='days')


class Week(Frequency):
    def __init__(self):
        Frequency.__init__(self, pandas_alias='W',
                           friendly_name='Week',
                           timedelta_key='weeks')


class Month(Frequency):

    def __init__(self):
        Frequency.__init__(self, pandas_alias='M',
                           friendly_name='End of Month',
                           timedelta_key='months')


class MonthStart(Frequency):

    def __init__(self):
        Frequency.__init__(self, pandas_alias='MS',
                           friendly_name='End of Month',
                           timedelta_key='months')


class Annual(Frequency):

    def __init__(self):
        Frequency.__init__(self, pandas_alias='MS',
                           friendly_name='Year Start',
                           timedelta_key='years')