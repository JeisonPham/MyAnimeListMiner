#!/usr/bin/env python
# coding: utf-8

# In[5]:


import json
import requests
import time

header = ['Title','type','genre','duration','source','producers','studios','score']


# In[6]:


import pygsheets
#authorization
gc = pygsheets.authorize(service_file='client_secret.json')

#open the google spreadsheet (where 'PY to Gsheet Test' is the name of my sheet)
sh = gc.open('Myanimelist')

wks = sh[0]
wks.update_row(1,values=header)


# In[7]:


mal_index = 0
spread_index = 2
status_error = []


# In[8]:


while len(status_error) < 100:
    mal_index += 1
    url = "https://api.jikan.moe/v3/anime/{}".format(mal_index)
    response = requests.get(url)
    print(mal_index, end=" ")
    # Print the status code of the response.
    status = response.status_code
    
    if status == 200:
        data = response.json()
        
        producers = ""
        for i in data['producers']:
            producers += "{}, ".format(i['mal_id'])
            
        licensors = ""
        for i in data['licensors']:
            licensors += "{}, ".format(i['mal_id'])
            
        studios = ""
        for i in data['studios']:
            studios += "{}, ".format(i['mal_id'])
            
        genres = ""
        for i in data['genres']:
            genres += "{}, ".format(i['mal_id'])
            
        info = [data['title'],data['type'],genres,data['duration'],data['source'], producers, studios,data['score']]
        
        wks.update_row(spread_index,values=info)
        spread_index += 1
        
        status_error = []
    elif status == 404:
        status_error.append(status)
        print(len(status_error), end=" ")
    elif status == 429:
        mal_index -= 1
        continue
    print(status)
    time.sleep(1)

