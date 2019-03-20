from datetime import datetime
import pandas as pd
import numpy as np
import config


def Data_transform():

	global authorname_list
	global time_start
	global time_end

	time_start = config.time_start
	time_end = config.time_end
	authorname_list = config.authorname_list

	print(authorname_list)
	print(time_start)
	print(time_end)

	df=pd.read_csv('APIOutput.csv')

	df['month-date']=df['timestamp'].apply(lambda x: datetime.utcfromtimestamp(int(x/1000)).strftime('%b-%d'))
	df['year-month-date']=df['timestamp'].apply(lambda x: datetime.utcfromtimestamp(int(x/1000)).strftime('%Y-%m-%d'))

	print(df.head())

	
	# lookback = (datetime.now() + relativedelta(months=-lookback_period)).strftime('%Y-%m-%d')

	# df_new = df[df['year-month-date']>=lookback]

	df_new = df[(df['year-month-date']>=time_start) & (df['year-month-date']<=time_end) & (df['author_displayName'].isin(authorname_list))]

	print(df_new.head())
	
	df_temp=df_new[['month-date','author_displayName']].rename(columns={'author_displayName':'author'})

	df_temp.to_csv('BitBucketDashboardInput.csv')