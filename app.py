#!/usr/bin/env python
# coding: utf-8

# In[7]:


import pandas as pd
import json
import requests
import time

headers = ["Title"]
for i in range(1,44):
    headers.append(i)
headers.append("Score")
headers.append("Type")


# In[12]:


df = pd.DataFrame(columns=headers)
index = 13625
status_error = []


# In[13]:


while len(status_error) < 100:
    index += 1
    url = "https://api.jikan.moe/v3/anime/{}".format(index)
    response = requests.get(url)
    print(index, end=" ")
    # Print the status code of the response.
    status = response.status_code
    
    if status == 200:
        data = response.json()
        series = [0] * len(df.columns)
        series[0] = data["title"]
        series[-2] = data["score"]
        series[-1] = data["type"]
        for i in data["genres"]:
            series[i['mal_id']]  = 1
        df.loc[len(df.index)] = series
        print(len(df.index), end =" ")
        status_error = []
    elif status == 404:
        status_error.append(status)
        print(len(status_error), end=" ")
    elif status == 429:
        index = index - 1
        continue
    print(status)
    time.sleep(1)


# In[14]:


df.tail()


# In[ ]:


len(status_error)


# In[15]:


# df.to_csv("anime {}.csv".format(index), encoding='utf-8',index=False)


# In[15]:


import pygsheets
import pandas as pd
#authorization
gc = pygsheets.authorize(service_file='client_secret.json')

#open the google spreadsheet (where 'PY to Gsheet Test' is the name of my sheet)
sh = gc.open('Myanimelist')

#select the first sheet 
wks = sh[0]

#update the first sheet with df, starting at cell B2. 
wks.set_dataframe(df,(1,1))

