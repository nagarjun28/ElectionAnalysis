import pandas as pd
from pandas import Series,DataFrame
import numpy as np

# For visualization
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')
import requests
from io import StringIO
from datetime import datetime

url = "http://elections.huffingtonpost.com/pollster/2012-general-election-romney-vs-obama.csv"
source = requests.get(url).text
poll_data = StringIO(source)
poll_df = pd.read_csv(poll_data)

sns.factorplot('Affiliation',data=poll_df,kind='count')
sns.factorplot('Affiliation',data=poll_df,kind='count',hue='Population')
avg = pd.DataFrame(poll_df.mean())
avg.drop('Number of Observations',axis=0,inplace=True)

std = pd.DataFrame(poll_df.std())
std.drop('Number of Observations',axis=0,inplace=True)

avg.plot(yerr=std,kind='bar',legend=False)

poll_avg = pd.concat([avg,std],axis=1)
poll_avg.columns = ['Average','STD']
poll_avg.drop('Question Text',axis=0,inplace=True)
poll_avg.drop('Question Iteration',axis=0,inplace=True)
poll_avg.drop('Other',axis=0,inplace=True)

poll_df.plot(x='End Date',y=['Obama','Romney','Undecided'],linestyle='',marker='o')
poll_df['Difference'] = (poll_df.Obama - poll_df.Romney)/100

poll_df = poll_df.groupby(['Start Date'],as_index=False).mean()
poll_df.plot('Start Date','Difference',figsize=(12,4),linestyle='-')
row_in = 0
xlimit = []

for date in poll_df['Start Date']:
    if date[0:7] == '2012-10':
        xlimit.append(row_in)
        row_in+=1
    else:
        row_in+=1
poll_df.plot('Start Date','Difference',figsize=(12,4),linestyle='-',marker='o',xlim=(325,352))
plt.axvline(x=325+2,linewidth=4,color='grey')
plt.axvline(x=325+10,linewidth=4,color='grey')
plt.axvline(x=325+21,linewidth=4,color='grey')