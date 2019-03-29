import json
import requests
from datetime import datetime
import pandas as pd
import numpy as np
import os.path
# import config
import yaml


# 
# URL=  config.URL
# ACCESS_TOKEN = config.ACCESS_TOKEN
# time_start = config.time_start
# time_end = config.time_end
# project_list = config.project_list

with open("config.yaml", 'r') as stream:
    try:
        # print()
        content = yaml.load(stream)
        URL = content['URL']
        ACCESS_TOKEN = content['ACCESS_TOKEN']
        project_list = content['project_list']
        time_start = content['time_start']
        time_end = content['time_end']

    except yaml.YAMLError as exc:
        print(exc)


page_limit = 25


def BitBucketAPIcall():
    # print('hello world!')
    
    project_repo_pair = get_repo_list()
    # print('------------------------------------------- project, repo pairs --------------------------------------------')
    # print(project_repo_pair)
    # print('length of repos:', len(project_repo_pair))

    df=pd.DataFrame(columns=['project','repo','timestamp','year_month_date','author_name','author_emailAddress','author_slug','author_id','author_displayName'])
    
    for project,repo in project_repo_pair:

        print('----------------------------------  new project: {} repo: {} -----------------------------------------'.format(project,repo))
    #     print('ENDPOINT2:',ENDPOINT2)
        project_name = project
        repo_name = repo
        ENDPOINT2 = 'projects/{}/repos/{}/commits'.format(project,repo)    

        df_repo = get_commits_from_repo(ENDPOINT2,project,repo)
        df=df.append(df_repo)

    if not os.path.isfile('filename.csv'):
        df.to_csv('filename.csv',index=False)

    else: 
        df_temp=pd.read_csv('filename.csv')
        df=df.append(df_temp)
        df=df.drop_duplicates()
        df.to_csv('filename.csv',index=False)


def construct_url(endpoint):
    return '/'.join([URL, endpoint])


def basic_oauth(ENDPOINT,PARAMS):
    headers = {'Authorization': ACCESS_TOKEN}
    response = requests.get(construct_url(ENDPOINT),headers=headers,params=PARAMS)
    return response


def get_repo_list():

    repos_slug=[]
    repos_id=[]
    repos_name=[]
    project_repo=[]

    for project in project_list:

        ENDPOINT1 = 'projects/{}/repos'.format(project)

        start=0
        lastpage=False
        counter=0

        while not lastpage:
            print(not lastpage)
            print(counter)
            print(start)
            PARAMS={'limit':page_limit, 'start': start}
            response = basic_oauth(ENDPOINT1, PARAMS)
           
            for i in response.json()['values']:

                project_repo.append((project,i['slug']))
                repos_slug.append(i['slug'])
                repos_id.append(i['id'])
                repos_name.append(i['name'])
                
            counter+=1
            lastpage=response.json()['isLastPage']
            if not lastpage:
                start=response.json()['nextPageStart']

    return project_repo


def add_value(project_name,repo_name,response2):
    global earliest_commit
    # global project_name
    # global repo_name

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
            year_month_date.append(datetime.utcfromtimestamp(int(i['authorTimestamp']/1000)).strftime('%Y-%m-%d'))

        except:
            print('no timestamp info')
            timestamp.append(np.nan)
            year_month_date.append(np.nan)
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
        
    df_response = pd.DataFrame(
    {
     'project':project_list,
     'repo':repo_list,
     'timestamp':timestamp,
     'year_month_date':year_month_date,
     'author_name': author_name,
     'author_emailAddress':author_emailAddress,
     'author_slug':author_slug,
     'author_id':author_id,
     'author_displayName':author_displayName        
    })
    
    
    earliest_commit = min(year_month_date)
    print('updated earliest commit time:',earliest_commit)
    print('-------------------------------------------df_resonse is ----------------------------------------------------------------')
    print(df_response)
   
    return df_response


def get_commits_from_repo(ENDPOINT2,project,repo):

    global earliest_commit

    start = 0
    lastpage = False
    counter = 0
    earliest_commit = time_end
    df_repo=pd.DataFrame()
    
    while (not lastpage) and (earliest_commit >= time_start):
        print('----------------- page {} of project: {} repo: {}-----------------'.format(counter+1,project,repo))
        print('earliest commit time:',earliest_commit)
        print('is lastpage:',lastpage)
        print('counter:',counter)
        print('start:',start)
        
        PARAMS={'limit':page_limit, 'start': start}

        try:
            RESPONSE2 = basic_oauth(ENDPOINT2,PARAMS)
            print(RESPONSE2.json())
        except:
            print('no API response')
            break

    #     response = basic_oauth(ENDPOINT1, PARAMS)
        try:
#             print(RESPONSE2.json()['values'])
            df_response = add_value(project,repo,RESPONSE2)
            df_repo = df_repo.append(df_response)

            counter+=1
            lastpage=RESPONSE2.json()['isLastPage']
            print('updated lastpage:',lastpage)
            if not lastpage:
                start=RESPONSE2.json()['nextPageStart']
                print('next page start:',start)
        except:
            print('empty response values')
            break

    print('-------------------------------------------df_repo is ----------------------------------------------------------------')
    print(df_repo)

    return df_repo




