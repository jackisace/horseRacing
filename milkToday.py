
from argparse import _MutuallyExclusiveGroup
from bs4 import BeautifulSoup
import requests
import re
from structure import *
from raceParser import *
import datetime
import random
import time



url = "https://www.racingpost.com/results/"

urlhtml = requests.get(url)
soupthisDate = urlhtml.text
dateSoup = BeautifulSoup(soupthisDate, 'html.parser')

raceURLs = []

for item in dateSoup.find_all('a', {'class':"rp-raceCourse__panel__race__info__buttons__link"}): # FOR EACH RACE
    page = str(item).split('href="')[1]
    page = page.split('">')[0]
    raceURLs.append(str("https://www.racingpost.com" + page))



for raceURL in raceURLs:
    print(raceURL)
    raceHtml = requests.get(raceURL)
    parsePage(raceHtml, raceURL)


