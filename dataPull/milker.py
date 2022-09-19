
from argparse import _MutuallyExclusiveGroup
from bs4 import BeautifulSoup
import requests
import re
from structure import *
from raceParser import *
import datetime
import random
import time


#GLOBALS



lastURL = "https://www.racingpost.com/results/416/sha-tin/2021-03-07/779774"
START = False

lastDate = lastURL.split("/")[-2]
print(lastDate)
DATESTART = False


datetime_object = datetime.datetime.now()

url = "https://www.racingpost.com/results/DATE"

URLs = []

for i in range(6200): # 6200
    datetime_object = datetime_object - datetime.timedelta(days=1)
    date = (str(datetime_object).split(" ")[0])
    URLs.append(url.replace("DATE", date))


for URL in URLs: # FOR EACH DATE
    print(URL)
    if lastDate in URL:
        DATESTART = True

    if DATESTART:
        raceURLs = []
        urlhtml = requests.get(URL)
        soupthisDate = urlhtml.text
        dateSoup = BeautifulSoup(soupthisDate, 'html.parser')
        
        for item in dateSoup.find_all('a', {'class':"rp-raceCourse__panel__race__info__buttons__link"}): # FOR EACH RACE
            page = str(item).split('href="')[1]
            page = page.split('">')[0]
            raceURLs.append(str("https://www.racingpost.com" + page))

        

        for raceURL in raceURLs:
            if raceURL == lastURL:
                START = True
            if START:
                print(raceURL)
                raceHtml = requests.get(raceURL)
                parsePage(raceHtml, raceURL)



        
