from dateutil import rrule


class RecurringEvent(object):

    def __new__(cls, *args, **kwargs):
        count = kwargs.get('count')

    def __init__(self, freq,
                 count=None,
                 interval=1,
                 wkst=None,
                 bysetpos=None,
                 bymonth=None,
                 bymonthday=None,
                 byyearday=None,
                 byeaster=None,
                 byweekno=None,
                 byweekday=None,
                 byhour=None,
                 byminute=None,
                 bysecond=None):
        self.freq = freq
        self.rrule_data = {'interval': interval,
                           'wkst': wkst,
                           'bysetpos': bysetpos,
                           'bymonth': bymonth,
                           'bymonthday': bymonthday,
                           'byyearday': byyearday,
                           'byeaster': byeaster,
                           'byweekno': byweekno,
                           'byweekday': byweekday,
                           'byhour': byhour,
                           'byminute': byminute,
                           'bysecond': bysecond}


class SecondlyEvent(RecurringEvent):
    def __init__(self, **kwargs):
        RecurringEvent.__init__(freq=rrule.SECONDLY, **kwargs)


class MinutelyEvent(RecurringEvent):
    def __init__(self, **kwargs):
        RecurringEvent.__init__(freq=rrule.MINUTELY, **kwargs)


class HourlyEvent(RecurringEvent):
    def __init__(self, **kwargs):
        RecurringEvent.__init__(freq=rrule.HOURLY, **kwargs)


class DailyEvent(RecurringEvent):

    def __init__(self, **kwargs):
        RecurringEvent.__init__(freq=rrule.DAILY, **kwargs)


class WeeklyEvent(RecurringEvent):
    def __init__(self, **kwargs):
        RecurringEvent.__init__(freq=rrule.WEEKLY, **kwargs)


class YearlyEvent(RecurringEvent):
    def __init__(self, **kwargs):
        RecurringEvent.__init__(freq=rrule.YEARLY, **kwargs)



