from collections import defaultdict

import pandas as pd
from tabulate import tabulate


class ResultSet(object):

    def __init__(self, name):
        self.name = name
        self._results = dict()
        self._table_data = list()
        self.result_tables = defaultdict(list)
        self.summary_results = dict()

    def add_summary_results(self, **results):
        for result_name, result_val in results.items():
            self.summary_results[result_name] = result_val
            setattr(self, result_name, result_val)

    def add_table_results(self, table_name, **results):
        self.result_tables[table_name].append(results)

    def add_results(self, **results):
        for result_name, result_val in results.items():
            self._results[result_name] = result_val
            setattr(self, result_name, result_val)

    def add_result_row(self, **row_data):
        self._table_data.append(row_data)

    def summary(self):
        for result_name, result_val in self._results.items():
            print("%s: %s" % (result_name, result_val))
        result_df = pd.DataFrame(self._table_data)
        print(tabulate(result_df, headers='keys'))