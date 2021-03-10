'''Once we are comfortable with the data, and we know more or less what we are dealing with, I would like to look at how different clustering techniques will perform on this dataset.
all clustering techniques from https://scikit-learn.org/stable/modules/clustering.html will be tested, because why not!'''
import pandas as pd
import numpy as np

# csv file downloaded from https://archive.ics.uci.edu/ml/datasets/Bank%2BMarketing; ordered by date: from May 2008 to November 2010
customer_data = pd.read_csv('bank-additional-full.csv', delimiter=';')
customer_data.rename(columns={'y': 'subscribed'}, inplace=True)  # changing the last column to subscribed

# the following two lines help to look at the dataframes in a better view
pd.set_option('display.max_columns', 30)
pd.set_option('display.width', 1000)
