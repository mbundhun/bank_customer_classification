# Classifying customers of a Portuguese bank
Aim of project is to understand and predict customer behaviour. The data is about direct marketing campaigns, based on phone calls, of a Portuguese banking institution. Often, more than one contact to the same client was required, in order to access if the product (bank term deposit) would be ('yes') or not ('no') subscribed. The data was obtained from https://archive.ics.uci.edu/ml/datasets/Bank%2BMarketing.

# Input variables:
### bank client data:
1 - age (numeric)<br/>
2 - job : type of job (categorical: 'admin.','blue-collar','entrepreneur','housemaid','management','retired','self-employed','services','student','technician','unemployed','unknown')<br/>
3 - marital : marital status (categorical: 'divorced','married','single','unknown'; note: 'divorced' means divorced or widowed)<br/>
4 - education (categorical: 'basic.4y','basic.6y','basic.9y','high.school','illiterate','professional.course','university.degree','unknown')<br/>
5 - default: has credit in default? (categorical: 'no','yes','unknown')<br/>
6 - housing: has housing loan? (categorical: 'no','yes','unknown')<br/>
7 - loan: has personal loan? (categorical: 'no','yes','unknown')
### related with the last contact of the current campaign:
8 - contact: contact communication type (categorical: 'cellular','telephone')<br/>
9 - month: last contact month of year (categorical: 'jan', 'feb', 'mar', ..., 'nov', 'dec')<br/>
10 - day_of_week: last contact day of the week (categorical: 'mon','tue','wed','thu','fri')<br/>
11 - duration: last contact duration, in seconds (numeric). Important note: this attribute highly affects the output target (e.g., if duration=0 then y='no'). Yet, the duration is not known before a call is performed. Also, after the end of the call y is obviously known. Thus, this input should only be included for benchmark purposes and should be discarded if the intention is to have a realistic predictive model.
### other attributes:
12 - campaign: number of contacts performed during this campaign and for this client (numeric, includes last contact)<br/>
13 - pdays: number of days that passed by after the client was last contacted from a previous campaign (numeric; 999 means client was not previously contacted)<br/>
14 - previous: number of contacts performed before this campaign and for this client (numeric)<br/>
15 - poutcome: outcome of the previous marketing campaign (categorical: 'failure','nonexistent','success')
### social and economic context attributes
16 - emp.var.rate: employment variation rate - quarterly indicator (numeric)<br/>
17 - cons.price.idx: consumer price index - monthly indicator (numeric)<br/>
18 - cons.conf.idx: consumer confidence index - monthly indicator (numeric)<br/>
19 - euribor3m: euribor 3 month rate - daily indicator (numeric)<br/>
20 - nr.employed: number of employees - quarterly indicator (numeric)

# Output variable (desired target):
21 - y - has the client subscribed a term deposit? (binary: 'yes','no')

# Data exploration
The dataset containts 41188 rows and 21 columns, as described above. Do the rows contain different marketing call information on the same customer? -> this has to be checked; there is no indication on that. It is interesting to also note that the variable 'duration' is an endogenous variable. This is because, customers who will agree to a term deposit will naturally talk more on the phone, while someone who will say no to a term deposit will do that rather quickly. Hence, the duration is more of an outcome of their decision to say yes or no to the term deposit. \
![image](https://user-images.githubusercontent.com/48698645/109701177-03420780-7b93-11eb-8b34-88af0ec7598b.png)

