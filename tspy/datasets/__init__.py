import os

from tspy.time_series import TimeSeries

DATASET_DIR = os.path.dirname(os.path.realpath(__file__))

female_births_ca = TimeSeries.from_csv(csv_path='%s/female_births.csv' % DATASET_DIR, freq='D', var_name='births', date_fmt='%Y-%m-%d')