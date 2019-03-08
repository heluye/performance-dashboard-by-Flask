import json
import requests


#try this first 
URL=  'https://api.bitbucket.org/2.0'
ENDPOINT = 'user'
ACCESS_TOKEN = 'token OTk2NTk1MTA0MDczOhxMKpn4xWkRS8ixN51Ve+4gSxxe'


# #if the first section didn't work, then try this
# URL=  'https://adlm.nielsen.com'
# ENDPOINT = 'rest/api/1.0/users'
# ACCESS_TOKEN = 'token OTk2NTk1MTA0MDczOhxMKpn4xWkRS8ixN51Ve+4gSxxe'


def construct_url(endpoint):
    return '/'.join([URL, endpoint])


def basic_oauth():
    headers = {'Authorization': ACCESS_TOKEN}
    response = requests.get(construct_url(ENDPOINT),headers=headers)
    print(response.request.headers)
    print(response.text)
    print(response.status_code)
    print(response.url)


if __name__ == '__main__':
	basic_oauth()