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
                           friendly_name='Start of Month',
                           timedelta_key='months')


class SemiMonthEnd(Frequency):

    def __init__(self):
        Frequency.__init__(self, pandas_alias='SM',
                           friendly_name='Semi-month end frequency (15th and end of month)')


class SemiMonthStart(Frequency):

    def __init__(self):
        Frequency.__init__(self, pandas_alias='SMS',
                           friendly_name='Semi-month start frequency (1st and 15th)')


class BusinessMonthEnd(Frequency):

    def __init__(self):
        Frequency.__init__(self, pandas_alias='BM',
                           friendly_name='Business month end frequency')


class Quarter(Frequency):

    def __init__(self):
        Frequency.__init__(self, pandas_alias='Q',
                           friendly_name='Quarter end frequency')


class BusinessQuarter(Frequency):

    def __init__(self):
        Frequency.__init__(self, pandas_alias='BQ',
                           friendly_name='Business quarter end frequency')


class QuarterStart(Frequency):

    def __init__(self):
        Frequency.__init__(self, pandas_alias='QS',
                           friendly_name='Quarter start frequency')


class BusinessQuarterStart(Frequency):

    def __init__(self):
        Frequency.__init__(self, pandas_alias='BQS',
                           friendly_name='Business quarter start frequency')


class Year(Frequency):

    def __init__(self):
        Frequency.__init__(self, pandas_alias='A',
                           friendly_name='Year end frequency',
                           timedelta_key='years')


class YearStart(Frequency):

    def __init__(self):
        Frequency.__init__(self, pandas_alias='AS',
                           friendly_name='Year start frequency',
                           timedelta_key='years')


class BusinessYear(Frequency):

    def __init__(self):
        Frequency.__init__(self, pandas_alias='BA',
                           friendly_name='Business year end frequency',
                           timedelta_key='years')


class BusinessYearStart(Frequency):

    def __init__(self):
        Frequency.__init__(self, pandas_alias='BAS',
                           friendly_name='Business year start frequency',
                           timedelta_key='years')


class BusinessHour(Frequency):

    def __init__(self):
        Frequency.__init__(self, pandas_alias='BH',
                           friendly_name='Business hour frequency',
                           timedelta_key='hours')


class Hour(Frequency):

    def __init__(self):
        Frequency.__init__(self, pandas_alias='H',
                           friendly_name='Hour frequency',
                           timedelta_key='hours')


class Minute(Frequency):

    def __init__(self):
        Frequency.__init__(self, pandas_alias='T',
                           friendly_name='Minute frequency',
                           timedelta_key='minutes')


class Second(Frequency):

    def __init__(self):
        Frequency.__init__(self, pandas_alias='S',
                           friendly_name='Second frequency',
                           timedelta_key='seconds')


class MilliSecond(Frequency):

    def __init__(self):
        Frequency.__init__(self, pandas_alias='ms',
                           friendly_name='Millisecond frequency',
                           timedelta_key='milliseconds')


class MicroSecond(Frequency):

    def __init__(self):
        Frequency.__init__(self, pandas_alias='us',
                           friendly_name='Microsecond frequency',
                           timedelta_key='microseconds')


class NanoSecond(Frequency):

    def __init__(self):
        Frequency.__init__(self, pandas_alias='N',
                           friendly_name='Nanosecond frequency')