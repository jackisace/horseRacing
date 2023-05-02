from bs4 import BeautifulSoup
import requests
from structure import *
from raceParserTomorrow import *
import os

URL = "https://www.racingpost.com/racecards/tomorrow"


print(URL)
urlhtml = requests.get(URL)
soupthisDate = urlhtml.text
dateSoup = BeautifulSoup(soupthisDate, 'html.parser')

raceURLs = []
for item in dateSoup.find_all('a', {'class':"RC-meetingItem__link"}): # FOR EACH RACE
    page = str(item).split('href="')[1]
    page = page.split('">')[0]
    raceURLs.append(str("https://www.racingpost.com" + page))



for raceURL in raceURLs:
    print(raceURL)
    raceHtml = requests.get(raceURL)
    parsePage(raceHtml, raceURL)
        
