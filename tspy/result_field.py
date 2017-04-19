from abc import abstractmethod


import pandas as pd
import tabulate


class ResultField(object):

    def __init__(self, name, is_summary_field=True):
        self.name = name
        self.is_summary_field = is_summary_field
        self.value = None

    def __str__(self):
        return self.summary_str

    def __set__(self, instance, value):
        self.value = value

    @property
    @abstractmethod
    def summary_str(self):
        pass


class FloatField(ResultField):

    def __init__(self, name, summary_round=4, is_summary_field=True):
        self.summary_round = summary_round
        ResultField.__init__(self, name=name, is_summary_field=is_summary_field)

    @property
    def summary_str(self):
        return "{name}: {value}".format(name=self.name, value=round(self.value, self.summary_round))

    def __get__(self, instance, owner):
        return self.value


class TableField(ResultField):

    def __init__(self, name, columns):
        self.columns = columns
        self._data = list()
        ResultField.__init__(self, name=name, is_summary_field=False)

    def df(self):
        return pd.DataFrame(self._data)

    def add_row(self, **kwargs):
        self._data.append(kwargs)

    @property
    def summary_str(self):
        return "{title} \n \n {table}".format(title=self.name,
                                              table=tabulate.tabulate(self.df(), headers='keys', tablefmt='psql'))