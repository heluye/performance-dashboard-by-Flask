from datetime import datetime
import pandas as pd
import numpy as np
# import config
import yaml


# time_start = config.time_start
# time_end = config.time_end

with open("config.yaml", 'r') as stream:
    try:
        # print()
        content = yaml.load(stream)
        time_start = content['time_start']
        time_end = content['time_end']

    except yaml.YAMLError as exc:
        print(exc)


def Data_transform():

	df_author = pd.read_csv('group_member_list.csv')

	lan_id_list = df_author['LAN ID'].tolist()

	print(df_author.head())

	print(lan_id_list)
	print(time_start)
	print(time_end)

	df=pd.read_csv('filename.csv')

	df['month-date']=df['timestamp'].apply(lambda x: datetime.utcfromtimestamp(int(x/1000)).strftime('%b-%d'))

	print(df.head())

	df_new = df[(df['year_month_date']>=time_start) & (df['year_month_date']<=time_end) & (df['author_name'].isin(lan_id_list))]

	print(df_new.head())
	
	df_temp=df_new[['year_month_date','month-date','author_displayName','project','repo']].rename(columns={'author_displayName':'author'})

	df_temp.to_csv('BitBucketDashboardInput.csv',index=False)