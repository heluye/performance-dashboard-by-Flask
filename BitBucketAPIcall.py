import json
import requests
from datetime import datetime
import pandas as pd
import numpy as np
import config

def construct_url(endpoint):
    return '/'.join([URL, endpoint])

def basic_oauth(ENDPOINT,PARAMS):
    headers = {'Authorization': ACCESS_TOKEN}
    response = requests.get(construct_url(ENDPOINT),headers=headers,params=PARAMS)
    return response

def get_repo_list(ENDPOINT1):
    start=0
    lastpage=False
    counter=0

    repos_slug=[]
    repos_id=[]
    repos_name=[]

    while not lastpage:
        print(not lastpage)
        print(counter)
        print(start)
        PARAMS={'limit':25, 'start': start}
        response = basic_oauth(ENDPOINT1, PARAMS)
       
        for i in response.json()['values']:
            repos_slug.append(i['slug'])
            repos_id.append(i['id'])
            repos_name.append(i['name'])
            
        counter+=1
        lastpage=response.json()['isLastPage']
        if not lastpage:
            start=response.json()['nextPageStart']
    return repos_slug

def add_value(response2):
    global earliest_commit
    global project_name
    global repo_name

    month_date=[]
    year_month_date=[]
    timestamp=[]
    
    author_name=[]
    author_emailAddress=[]
    
    author_slug=[]
    author_id=[]
    author_displayName=[]

    repo_list=[]
    project_list=[]

    for i in response2.json()['values']:

        project_list.append(project_name)
        repo_list.append(repo_name)

        try:
            timestamp.append(i['authorTimestamp'])

        except:
            print('no timestamp info')
            timestamp.append(np.nan)
#             print(timestamp)
            pass
    
        try:            
            author_name.append(i['author']['name'])
        except:
            print('no author name')
            author_name.append(np.nan)
            pass
    
        try:            
            author_emailAddress.append(i['author']['emailAddress'])
        except:
            print('no author email')
            author_emailAddress.append(np.nan)
            pass 

        try:
            author_slug.append(i['author']['slug'])
        except:
            print('no author slug')
            author_slug.append(np.nan)
            pass
        
        try:
            author_id.append(i['author']['id'])
        except:
            print('no author id')
            author_id.append(np.nan)
            pass
        
        try:
            author_displayName.append(i['author']['displayName'])
        except:
            print('no author display name')      
            author_displayName.append(np.nan)
            print(i['author']['name'])
            pass 
        
    df1 = pd.DataFrame(
    {
     'project':project_list,
     'repo':repo_list,
     'timestamp':timestamp,
     'author_name': author_name,
     'author_emailAddress':author_emailAddress,
     'author_slug':author_slug,
     'author_id':author_id,
     'author_displayName':author_displayName        
    })
    
    
    earliest_commit = datetime.utcfromtimestamp(int(min(timestamp)/1000)).strftime('%Y-%m-%d')
    print('updated earliest commit time:',earliest_commit)
   
    return df1


def get_commits_from_repo(ENDPOINT2,df,repo):
    # global lastpage
    # global counter
    # global start
    # global ENDPOINT2
    # global df
    global earliest_commit

    start = 0
    lastpage = False
    counter = 0
    earliest_commit = time_end
    
    while (not lastpage) and (earliest_commit >= time_start):
        print('----------------- page {} of {} -----------------'.format(counter+1,repo))
        print('earliest_commit:',earliest_commit)
        print('lastpage:',lastpage)
        print('counter:',counter)
        print('start:',start)
        
        PARAMS={'limit':25, 'start': start}

        try:
            RESPONSE2 = basic_oauth(ENDPOINT2,PARAMS)
#             print(RESPONSE2.json())
        except:
            print('no API response')
            continue

    #     response = basic_oauth(ENDPOINT1, PARAMS)
        if RESPONSE2.json()['values']!=[]:
#             print(RESPONSE2.json()['values'])
            df_add = add_value(RESPONSE2)
            df = df.append(df_add)

            counter+=1
            lastpage=RESPONSE2.json()['isLastPage']
            print('updated lastpage:',lastpage)
            if not lastpage:
                start=RESPONSE2.json()['nextPageStart']
                print('next page start:',start)
        else:
            print('empty response values')
            break


    return df



def BitBucketAPIcall():
    global URL
    global ENDPOINT1
    global ACCESS_TOKEN
    global time_start
    global time_end
    global project_name 
    global repo_name


    # URL=  'https://adlm.nielsen.com/bitbucket/rest/api/1.0'
    # ENDPOINT1 = 'projects/WDS/repos'
    # ACCESS_TOKEN = 'Bearer OTk2NTk1MTA0MDczOhxMKpn4xWkRS8ixN51Ve+4gSxxe'
    # time_start = '2019-02-20'
    # time_end = '2019-03-20'

    URL=  config.URL
    ENDPOINT1 = config.ENDPOINT1
    ACCESS_TOKEN = config.ACCESS_TOKEN
    time_start = config.time_start
    time_end = config.time_end

    repos_slug = get_repo_list(ENDPOINT1)

    df=pd.DataFrame(columns=['project','repo','timestamp','author_name','author_emailAddress','author_slug','author_id','author_displayName'])
    for i in repos_slug:
        print('----------------------------------  new repo: {} -----------------------------------------'.format(i))
    #     print('ENDPOINT2:',ENDPOINT2)
        # start=0
        # lastpage=False
        # counter=0
        # earliest_commit = time_end
        project_name = 'WDS'
        repo_name = i
        ENDPOINT2 = 'projects/WDS/repos/{}/commits'.format(i)    
        df = get_commits_from_repo(ENDPOINT2,df,i)
        df.to_csv('APIOutput.csv')
