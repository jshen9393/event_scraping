# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 16:22:43 2016

@author: Jimmy

Outline of program

phase 1:
get webpage text
parse out links
parse event information from links


phase 2:
automate and script through events in future months
https://www.92y.org/calendar/index.aspx?monthDropDown=2016:3&kw=Event
Add or take away delta

To dos:
work on key words list: 

can't parse this:
<meta name="keywords" content="92nd Street Y,92Y,92ndStY,92StY,92Y,92YMHA,Breastfeeding Support Group" /> 
event_soup.find('meta',name='keywords')
find() got multiple values for argument 'name'
"""

import requests
import bs4
import re
import os
import json

street_address = '1395 Lexington Ave, New York, NY 10128'
domain = 'https://www.92y.org'

event_list = requests.get('https://www.92y.org/calendar/index.aspx?monthDropDown=2016:3&kw=Event')
list_soup = bs4.BeautifulSoup(event_list.text,'html.parser')
events = list_soup.find_all("a",class_='detailtip_trigger title')

list_links = []

for link in events:
    list_links = list_links
    list_links.append(link.get('href'))

data_points = ['event_link','title','presenter','description','image_link','date','location','price','venue']

list_link = list_links[5]
event_link= domain + list_link
event_request = requests.get(event_link)
event_soup =  bs4.BeautifulSoup(event_request.text,'html.parser')


if event_soup.find('meta',property = 'og:title')['content'] == None:
    title = None
else:
    title = event_soup.find('meta',property = 'og:title')['content']

if event_soup.find('div', class_="wrapper-banner").h2 == None:
    presenter = None
else:
    presenter = event_soup.find('div', class_="wrapper-banner").h2.getText()

if event_soup.h3 == None:
    description = None
else:
    description = event_soup.h3.text.strip()

if event_soup.find('div', class_="wrapper-banner").img['src'] == None:
    image_link = None
else:
    image_link = domain + event_soup.find('div', class_="wrapper-banner").img['src']

info = event_soup.find_all('div', class_="info-col")
info = bs4.BeautifulSoup(str(info),'html.parser')

date_raw = info.find_all('strong',string='Date:')
date_list = []
for x in range(0,len(date_raw)):
    date_add = date_raw[x].next_sibling.strip()
    date_list.append(date_add)

location_raw = info.find_all('strong',string='Location:')
location_list = []
for x in range(0,len(location_raw)):
    location_add = location_raw[x].next_sibling.strip()
    if location_add == 'Lexington Avenue at 92nd St':
        location_add = street_address
    else:
        location_add
    location_list.append(location_add)

price_raw = info.find_all('strong',string='Price:')
price_list = []
for x in range(0,len(price_raw)):
    price_add = price_raw[x].next_sibling.strip()
    price_list.append(price_add)

venue_raw = info.find_all('strong',string='Venue:')
venue_list = []
for x in range(0,len(venue_raw)):
    venue_add = venue_raw[x].next_sibling.strip()
    venue_list.append(venue_add)

os.chdir('C:\in')


for x in range(len(date_list)):
    event_dict = {}
    file = list_link.replace('/','_')
    for d in data_points:
        if d == 'event_link':
            event_dict[d] = event_link
        elif d =='title':
            event_dict[d] = title
        elif d == 'presenter':
            event_dict[d] = presenter
        elif d == 'description':
            event_dict[d] = description
        elif d == 'image_link':
            event_dict[d] = image_link
        elif d == 'date':
            event_dict[d] = date_list[x]
        elif d == 'location':
            event_dict[d]  = location_list[x]
        elif d == 'price':
            event_dict[d]  = price_list[x]
        elif d == 'venue':
            event_dict[d] = venue_list[x]
        else:
            event_dict[unknown] = 'unknown'
    filename = file+str(x)+'.json'
    with open (filename,'w') as outfile:
        json.dump((event_dict),outfile)








