

class Event(object):

    def __init__(self, date_time, name, pre_periods=0, post_periods=0):
        self.date_time = date_time
        self.name = name
        self.pre_periods = pre_periods
        self.post_periods = post_periods

