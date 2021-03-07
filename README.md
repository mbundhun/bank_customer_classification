# Classifying customers of a Portuguese bank
Aim of project is to understand, classify the customers and predict their behaviour. The data is about direct marketing campaigns, based on phone calls, of a Portuguese banking institution. Often, more than one contact to the same client was required, in order to access if the product (bank term deposit) would be ('yes') or not ('no') subscribed. The data was obtained from https://archive.ics.uci.edu/ml/datasets/Bank%2BMarketing.

# Input variables:
### bank client data:
1 - age (numeric)<br/>
2 - job : type of job (categorical: 'admin.','blue-collar','entrepreneur','housemaid','management','retired','self-employed','services','student','technician','unemployed','unknown')<br/>
3 - marital : marital status (categorical: 'divorced','married','single','unknown'; note: 'divorced' means divorced or widowed)<br/>
4 - education (categorical: 'basic.4y', 'basic.6y', 'basic.9y', 'high.school', 'illiterate', 'professional.course', 'university.degree', 'unknown')<br/>
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
The dataset containts 41188 rows and 21 columns, as described above. So question?: Are there rows that contain different marketing call information on the same customer? I have found no indication on that. So each row is interpreted as a unique customer/clients. Overall, there were 11% of clients who subscribed to a term deposit via this marketing campaign. It is interesting to also note that the variable 'duration' is an endogenous variable. This is because, customers who will agree to a term deposit will naturally talk more on the phone, while someone who will say no to a term deposit will do that rather quickly. Hence, the duration is more of an outcome of their decision to say yes or no to the term deposit. The difference in the call duration is shown in the density plot below.\
![image](https://user-images.githubusercontent.com/48698645/109701177-03420780-7b93-11eb-8b34-88af0ec7598b.png)

It would be interesting to look at how many customer were contacted over 2008 - 2010. As the data was sorted according to the data, I could create an approximately accurate indication of the specific dates for each observation. The date variable was generated using the _month_ and _day_of_week_ variables. The accuracy of those was validated and as contacts were done almost daily from March till December, the generated dates fitted the calendar really well such that the month has the correct number of days and that the day of month was coincided on the correct day of week. However, only the period around september/october wasnt clear as there seemed to be a break in the marketing campaign. However it was determined that this wouldnt affect the findingds from the time series. Down below is a graph that shows the total number of contacts performed per week. as the graph shows, Most of the contact, which is actually 67%, was done in 2008.\
![image](https://user-images.githubusercontent.com/48698645/110029441-c281f400-7d34-11eb-8e0c-7538aa6f1494.png)

Next, it would be interesting to see if there are any variables that can already explain the differences in the subscription behaviour. Down below, there are pair plots of numeric features that describe the customer, and each observation is categorised according to the output variable (y). Keep in mind that there are more than 40,000 data points, of which only 11% are term-deposit subscribers. So that graph might not be that clear.\
![image](https://user-images.githubusercontent.com/48698645/110150928-1d245a00-7de0-11eb-9bb5-8cc3eb772020.png)

Down below is a pairplot of the economic and social features.
![image](https://user-images.githubusercontent.com/48698645/110147550-1d225b00-7ddc-11eb-8a33-92db167383d0.png)
With these many datapoints, it is more difficult to find any pattern from the scatterplots. The density plots are more interesting to look at. We see that clients older than 60 are more interested in a term deposit on average. Another interesting finding is that it doesnt help to contact the client more than 23 times in this campaign, as no client contacted more than 23 times subscribed to the term deposit. So this is a improvement that the bank can already do for their next campaign. It is not so interesting to look at the density plot of pdays. From the density of the economic and social variables, clients are more likely to subscribe when the employment variation rate , the euribor and the nr. of employed is lower, and when the consumer confidence index is higher. (is this what we expected?)\

Down below is a heatmap to show the correlation between each numeric variables. 
![image](https://user-images.githubusercontent.com/48698645/110152782-6fff1100-7de2-11eb-9daa-83fe3ab01089.png)
There is some correlation amongst the economic and social features and a negative correlation between _pdays_ and _previous_. Nothing unexpected there.

