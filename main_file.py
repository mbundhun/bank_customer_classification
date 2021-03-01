import pandas as pd
import numpy as np

# csv file downloaded from https://archive.ics.uci.edu/ml/datasets/Bank%2BMarketing; ordered by date: from May 2008 to November 2010
customer_data = pd.read_csv('bank-additional-full.csv', delimiter=';')

# data exploration
pd.set_option('display.max_columns', 30)
pd.set_option('display.width', 1000)
customer_data.shape  # 41188 rows and 21 columns
customer_data.columns  # check data descriptions from url for column details
customer_data.info()  # checking the data types for each column
customer_data.isna().sum()  # no nan in the dataset
numeric_columns = ['age', 'duration', 'campaign', 'pdays', 'previous', 'emp.var.rate', 'cons.price.idx',
                   'cons.conf.idx', 'euribor3m', 'nr.employed']
np.isfinite(customer_data.loc[:, customer_data.columns.isin(numeric_columns)]).sum() - customer_data.shape[0]  # no infinite values in the numeric columns
customer_data.loc[:, customer_data.columns.isin(numeric_columns)].describe()  # looking at the high level distribution of the numeric columns
