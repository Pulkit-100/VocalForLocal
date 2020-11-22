#!/usr/bin/env python
# coding: utf-8

# In[4]:


input_file = "apps.csv"


# In[25]:


output_file = "apps2.csv"


# In[1]:


import pandas as pd
import numpy as np
import re


# In[2]:


import cloudinary
import cloudinary.uploader as uploader
from bs4 import BeautifulSoup
import requests
import base64


# In[3]:


cloudinary.config(
  cloud_name = "hmvh5jw7x",
  api_key = "355912947378767",
  api_secret = "EzVcH3FXVuRQh3eZjbvjWcqXEZg"
)


# In[5]:


try:
    df = pd.read_csv(input_file)
except:
    df = pd.read_csv(input_file,encoding='latin1')


# In[6]:


df


# In[7]:


df["Image"] = df["Image"].fillna('')


# In[8]:


def scrapImage(name, string = "brand logo"):
    fName = name.replace(" ","").replace("&","").replace("?","").replace("-","").replace(".","").replace("\n","").replace(";","")
    name = name.split()
    for i in string.split():
        name.append(i)
    link = "https://www.google.com/search?q={}&tbm=isch".format('+'.join(name))
    r=requests.get(link)
    soup=BeautifulSoup(r.content,'html.parser')
    try:
        mainSoup = soup.find_all("table",{"class":"GpQGbf"})[0]
        images = mainSoup.find_all("img")
        link = images[0].get('src')
    except Exception as E:
        print(E)
        print(fName)
        return None
    img = requests.get(link)
    image = img.content
    image = uploader.upload_resource(image, folder="Vocal4Local/{}".format(fName))
    return image.metadata["secure_url"]


# In[9]:


for i in df.iterrows():
    try:
        name = i[1]["Brand"]
        if i[1]["Image"]:
            continue
        image = scrapImage(name)
        print(i[0],name,image)
        df.at[i[0], 'Image'] = image
    except Exception as E:
        print(E)


# In[14]:


df


# In[21]:


df["Wiki"] = df["Wiki"].fillna('')
df["Country"] = df["Country"].fillna('')
df["Notes"] = df["Notes"].fillna('')


# In[18]:


for i in df.iterrows():
    if i[1]["Wiki"] or i[1]["Country"].upper() != "INDIA" :
        continue
    try:        
        name = i[1]["Brand"]
        name = name.split()
        name.append("Brand")
        name.append("wiki")
        link = "https://www.google.com/search?q={}".format('+'.join(name))
        r=requests.get(link)
        soup=BeautifulSoup(r.content,'html.parser')
        myDiv = soup.find_all("div",{"class":"BNeawe s3v9rd AP7Wnd"})
        wiki = myDiv[0].text.split('...')[0]
        wiki = wiki.split('.')
        if len(wiki)>1:
            wiki.pop()
        wiki = '.'.join(wiki)
        wiki+="."
        wiki = wiki.split("Contents")[0]
        wiki = wiki.split("\n")[0]
        print(i[0],i[1]["Brand"]," - ", wiki)
        df.at[i[0],"Wiki"] = wiki
    except Exception as E:
        print(E)
    


# In[22]:


df


# In[23]:


for i in df.iterrows():
    if i[1]["Notes"]=="":
        df.at[i[0],"Notes"] = i[1]["Category"]


# In[26]:


df.to_csv(output_file,index=False)


# In[ ]:




