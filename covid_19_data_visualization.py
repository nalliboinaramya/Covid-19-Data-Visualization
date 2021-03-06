# -*- coding: utf-8 -*-
"""Covid-19 Data visualization.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Ez15RqGBi7uvY2guWFEQxXOyUF23lsUA
"""

!pip install beautifulsoup4

from bs4 import BeautifulSoup #for parsing structured data
import requests #to retrieve website html data
import numpy as np
import pandas as pd
import csv

url = "https://www.worldometers.info/coronavirus/?utm_campaign=homeAdvegas1?%22%20%5Cl%22countries#countries"
html_page = requests.get(url).text#to retrieve html data

soup = BeautifulSoup(html_page,'lxml')# lxml is a parser creates a parser tree which helps to extract data from html

table = soup.find("table",id = "main_table_countries_today")# to find that specific HTML element by its ID
#print(table)

header_tags = table.find_all("th")#Find Elements by HTML Class Name
print(header_tags)
headers = [header.text.strip() for header in header_tags]
print(headers)

# to get the row of data from the table so that we can convert into csv file
rows = []
data_rows = table.find_all("tr")
#print(data_rows)
    
for row in data_rows:
  tag_value = row.find_all("td")
  stri_value = [tag.text.strip() for tag in tag_value]
  rows.append(stri_value)
print(rows)

with open('covid19_live_data.csv','w',newline = "") as output:
  writer = csv.writer(output)
  writer.writerow(headers)
  writer.writerows(rows)

import pandas as pd
import io
from google.colab import files
uploaded=files.upload()
df_covid_stats=pd.read_csv(io.BytesIO(uploaded['covid19_live_data.csv']))

print(df_covid_stats.to_string())

df_covid_stats.info()

df_covid_stats.shape

df_covid_stats.head()

"""***CLEANING COVID DATAFRAME***
1.  **Extracting required columns,rows**
2.  **Removing null values**


"""

df_required_stats= df_covid_stats[['Country,Other','TotalCases','TotalDeaths','TotalRecovered','ActiveCases']].copy()
print(df_required_stats.to_string())

df_required_stats.isnull().sum()

#Removing null values
df_required_stats.dropna(inplace = True)
print(df_required_stats.to_string())
print(df_required_stats.isnull().sum())
print(df_required_stats.shape)

df_required_stats.rename(columns = {'Country,Other':'Country'},inplace = True)
print(df_required_stats.to_string())

df_required_stats.duplicated().to_string()

#Removing unnecessary rows at the tail and Unnecessary columns
df_required_stats.drop([0,1,2,3,4,5,7,230,231,232,233,234,235,236,237],inplace = True)
print(df_required_stats.shape)

import pandas as pd
import io
from google.colab import files
uploaded=files.upload()
df_world_coordinates=pd.read_csv(io.BytesIO(uploaded['world_coordinates.csv']))

print(df_world_coordinates.to_string())

df_world_coordinates.shape

df_world_coordinates.info()

df_world_coordinates.isnull().sum()

final_data = pd.merge(df_world_coordinates,df_required_stats, how ='inner', on ='Country')
print(final_data.to_string())

import folium

map = folium.Map(location = [final_data.latitude.mean(),final_data.longitude.mean()],zoom_start = 1,control_scale = True)
tooltip = "click here!"
print(map)

for Country,lat,longi,total_cases,Death,Recov,Active in zip(list(final_data['Country']),list(final_data['latitude']),list(final_data['longitude']),list(final_data['TotalCases']),list(final_data['TotalDeaths']),list(final_data['TotalRecovered']),list(final_data['ActiveCases'])):
  folium.Marker(location = [lat,longi],
                  popup=folium.Popup(('<strong><b>State  : '+Country+'</strong> <br>' +
                    '<strong><b>Total Cases : '+total_cases+'</striong><br>' +
                    '<strong><font color= red>Deaths : </font>'+Death+'</striong><br>' +
                    '<strong><font color=green>Recoveries : </font>'+Recov+'</striong><br>' +
                    '<strong><b>Active Cases : '+Active+'</striong>' ),max_width=200),tooltip = tooltip).add_to(map)
#to show the map
map