import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import time
import resample

# csv file downloaded from https://archive.ics.uci.edu/ml/datasets/Bank%2BMarketing; ordered by date: from May 2008 to November 2010
customer_data = pd.read_csv('bank-additional-full.csv', delimiter=';')
customer_data.rename(columns={'y': 'subscribed'}, inplace=True)  # changing the last column to subscribed

# data exploration
pd.set_option('display.max_columns', 30)
pd.set_option('display.width', 1000)
customer_data.shape  # 41188 rows and 21 columns
customer_data.columns  # check data descriptions from url for column details
customer_data.info()  # checking the data types for each column
customer_data.isna().sum()  # no nan in the dataset
numeric_columns = ['age', 'duration', 'campaign', 'pdays', 'previous', 'emp.var.rate', 'cons.price.idx', 'cons.conf.idx', 'euribor3m', 'nr.employed']
np.isfinite(customer_data.loc[:, customer_data.columns.isin(numeric_columns)]).sum() - customer_data.shape[0]  # no infinite values in the numeric columns
customer_data.loc[:, customer_data.columns.isin(numeric_columns)].describe()  # looking at the high level distribution of the numeric columns
'''it looks like a lot of the data is skewed: age, duration, campaign, pdays and previous '''
plt.hist(customer_data.age, bins=max(customer_data.age) - min(customer_data.age) - 1)  # plotting age histogram, such that each age has its own bin
# sns.pairplot(customer_data.loc[:, customer_data.columns.isin(numeric_columns[:5])], markers='.', plot_kws={"s": 50})
sns.pairplot(customer_data.loc[:, customer_data.columns.isin(numeric_columns[:5] + ['subscribed'])], markers='.', hue='subscribed', plot_kws={"s": 50})  # pairplot with customer info
sns.pairplot(customer_data.loc[:, customer_data.columns.isin(numeric_columns[5:] + ['subscribed'])], markers='.', hue='subscribed', plot_kws={"s": 50})  # pariplot with social and economic attributes
'''Indicators of success with subcription: age >60, 1 contact only, no previous contact, low emp.var.rate, low cons.price.idx, and low nr.employed'''
'''pdays 999 has to be changed if it is to be included in the model'''
'''Note: duration will be treated as an endogenous variable'''
# share of poutcomes
prev_outcome_count_dict = {}
for o in customer_data.poutcome.unique():
    prev_outcome_count_dict[o] = round((customer_data.poutcome == o).mean(), 2) * 100
'''86% of customers were never contacted before'''
subscribed_count_dict = {}
for s in customer_data.subscribed.unique():
    subscribed_count_dict[s] = round((customer_data.subscribed == s).mean(), 2) * 100
# do we know why some people who did a term deposit before didnt want to do one this time? -> cus they still had money deposited?
# timeseries of poutcomes
customer_data['year'] = 2008
for i in range(1, customer_data.shape[0]):
    if (customer_data.month[i - 1] == 'dec') & (customer_data.month[i] == 'mar'):
        customer_data.loc[i:, 'year'] += 1


def wkday_to_num_during_week(wkday):
    return {'mon': 1, 'tue': 2, 'wed': 3, 'thu': 4, 'fri': 5, 'sat': 6, 'sun': 7}[wkday]


def wkday_to_num_after_wkend(wkday):
    return {'mon': 8, 'tue': 9, 'wed': 10, 'thu': 11, 'fri': 12}[wkday]


def month_to_num(short_month):
    return {'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
            'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12}[short_month]


first_wkday_of_month = datetime.date(customer_data.year[0], customer_data.loc[0, 'month (num)'], 1).strftime('%a').lower()
days_diff = wkday_to_num_after_wkend(customer_data.day_of_week[0]) - wkday_to_num_during_week(first_wkday_of_month) + 1
customer_data['month_date'] = days_diff

for i in range(1, customer_data.shape[0]):
    if customer_data.day_of_week[i - 1] != customer_data.day_of_week[i]:
        days_diff = wkday_to_num_during_week(customer_data.day_of_week[i]) - wkday_to_num_during_week(customer_data.day_of_week[i - 1])
        if days_diff < 0:
            days_diff = wkday_to_num_after_wkend(customer_data.day_of_week[i]) - wkday_to_num_during_week(customer_data.day_of_week[i - 1])
        customer_data.loc[i:, 'month_date'] += days_diff
    if customer_data.month[i - 1] != customer_data.month[i]:
        first_wkday_of_month = datetime.date(customer_data.year[i], customer_data.loc[i, 'month (num)'], 1).strftime('%a').lower()
        days_diff = wkday_to_num_during_week(customer_data.day_of_week[i]) - wkday_to_num_during_week(first_wkday_of_month) + 1
        if days_diff < 0:
            days_diff = wkday_to_num_after_wkend(customer_data.day_of_week[i]) - wkday_to_num_during_week(first_wkday_of_month) + 1
        customer_data.loc[i:, 'month_date'] = days_diff

table = pd.pivot_table(customer_data, index=['month (num)'], columns=['year'], values=['month_date'], aggfunc=np.max)
'''the date was manually validated and dates of oct 2008 should be displayed by 2 weeks and nov 2009 probably by 1 week. However, this wont cause major problems for interpretation
as the dates are in a continuous format and correct in that sense. So detecting trends, if any, should be possible'''

customer_data['month (num)'] = customer_data.month.apply(month_to_num)
df2 = customer_data[['year', 'month (num)', 'month_date']].copy()
df2.columns = ["year", "month", "day"]
customer_data['date'] = pd.to_datetime(df2)

# creating time series: e.g. grouping yes/no by day
total_yes_ts = (customer_data.subscribed == 'yes').groupby(customer_data.date).sum().resample('W', how='sum')
average_yes_ts = (customer_data.subscribed == 'yes').groupby(customer_data.date).mean().resample('W', how='mean')
total_no_ts = (customer_data.subscribed == 'no').groupby(customer_data.date).sum().resample('W', how='sum')
average_no_ts = (customer_data.subscribed == 'no').groupby(customer_data.date).mean().resample('W', how='mean')

# making plots
fig, axs = plt.subplots(2, 2)
axs[0, 0].plot(total_yes_ts.index, total_yes_ts)
axs[0, 0].set_title('Total nr. of YES over time')
axs[0, 0].set(ylabel='Total')
axs[0, 1].plot(total_no_ts.index, total_no_ts)
axs[0, 1].set_title('Total nr. of NO over time')
axs[1, 0].plot(average_yes_ts.index, average_yes_ts)
axs[1, 0].set(ylabel='Average')
axs[1, 0].set_title('Success rate of YES over time')
axs[1, 1].plot(average_no_ts.index, average_no_ts)
axs[1, 1].set_title('Rejection rate (NO) over time')

for ax in axs.flat:
    ax.set(xlabel='date')
plt.tight_layout()
