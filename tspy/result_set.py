from collections import defaultdict

import pandas as pd
from tabulate import tabulate


class ResultSet(object):

    def __init__(self, name):
        self.name = name
        self.result_tables = defaultdict(list)
        self.summary_results = dict()

    def add_summary_results(self, **results):
        for result_name, result_val in results.items():
            self.summary_results[result_name] = result_val
            setattr(self, result_name, result_val)

    def add_table_results(self, table_name, **results):
        self.result_tables[table_name].append(results)

    def _summary_table(self):
        table_data = [[k, v] for k, v in self.summary_results.items()]
        return tabulate(table_data)

    def summary(self):
        summary_table = "%s Summary \n%s\n" % (self.name, self._summary_table())
        print(summary_table)
        for result_table_name, table_data in self.result_tables.items():
            print('%s \n%s' % (result_table_name, tabulate(pd.DataFrame(table_data), headers='keys', tablefmt='psql')))