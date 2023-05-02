from argparse import _MutuallyExclusiveGroup
from bs4 import BeautifulSoup
import requests
import re
from structure import *
import datetime
import random
import time
import json
import pdb



def parseRace(url, raceInfo, numHorses):
    global currentRace
    currentRace = race(raceInfo, url)

    print("parsing {} horses from {}".format(numHorses, url))
    print("race info: {}".format(raceInfo))
    
    response = requests.get(url)
    soupthis = response.text
    soup = BeautifulSoup(soupthis, 'html.parser')

    start = str(soup).find('json">') + 6
    info = str(soup)[start:]
    end = info.find("</script>")
    info = info[:end]
    info = json.loads(info)
    horses = info["props"]["pageProps"]["race"]["rides"]
    for Horse in horses:
        try:
            name = str(Horse["horse"]["name"])
        except:
            name = None
        try:
            jockey = str(Horse["jockey"]["name"])
        except:
            jockey = None
        try:
            trainer = str(Horse["trainer"]["name"])
        except:
            trainer = None
        try:
            age = str(Horse["horse"]["age"])
        except:
            age = None
        try:
            topspeed = 0
        except:
            topspeed = None
        try:
            weights = str(Horse["handicap"])
        except:
            weights = None
        try:
            ors = 0
        except:
            ors = None
        try:
            price = str(Horse["betting"]["current_odds"])
        except:
            price = None
        try:
            country = "UK"
        except:
            country = None
        try:
            firstWeight = weights[0]
        except:
            firstWeight = None
        try:
            posLength = str(Horse["finish_distance"])
        except:
            posLength = None
        try:
            pedigrees = None
        except:
            pedigrees = None
        try:
            position = str(Horse["finish_position"])
        except:
            position = None
        try:
            startingPosition = str(Horse["cloth_number"])
        except:
            startingPosition = None
        try:
            RPR = None
        except:
            RPR = None
        try:
            MR = None
        except:
            MR = None
        try:
            Form = None
        except:
            Form = None

        
        #print(name, jockey, trainer, )
        horse(name,jockey,trainer,age,topspeed,weights,ors,price,country,firstWeight,posLength,pedigrees,position,startingPosition,RPR,MR,Form)
    
    currentRace.saveSL()
    return



datetime_object = datetime.datetime.now()

url = "https://www.sportinglife.com/racing/results/DATE"

URLs = []
numberOfDaysToMilk = 6200

for i in range(numberOfDaysToMilk): # 6200
    datetime_object = datetime_object - datetime.timedelta(days=1)
    date = (str(datetime_object).split(" ")[0])
    URLs.append(url.replace("DATE", date))


for URL in URLs: # FOR EACH DATE
    print(URL)
    raceURLs = []
    urlhtml = requests.get(URL)
    soupthisDate = urlhtml.text
    dateSoup = BeautifulSoup(soupthisDate, 'html.parser')

    #data-test-id="race-container"
    for item in dateSoup.find_all('div', {'data-test-id':"race-container"}): # FOR EACH RACE
        page = str(item).split('href="')[1]
        page = page.split('">')[0]
        raceURLs.append(str("https://www.sportinglife.com" + page))

    






    a = str(soupthisDate.split('application/json">')[1])
    a = a.split('</script>')[0]
    parsed = json.loads(a)

    url = "https://www.sportinglife.com/racing/racecards/DATE/PLACE/racecard/RACEID/NAME"
    urls = []
    for item in parsed["props"]["pageProps"]["meetings"]:
        for Race in item["races"]:
            numHorses = int(Race["ride_count"])
            time = str(Race["time"])
            date =  str(Race["date"])
            age = str(Race["age"])
            race_class = str(Race["race_class"])
            distance = str(Race["distance"])
            raceId = str(Race["race_summary_reference"]["id"])
            raceName = str(Race["name"])
            racePlace = str(Race["course_name"])
            URL = url.replace("DATE", date)
            URL = URL.replace("PLACE", racePlace)
            URL = URL.replace("RACEID", raceId)
            URL = URL.replace("NAME", raceName)
            URL = URL.replace(" ", "-").replace("(", "").replace(")", "").replace("'", "").replace('"','')
            urls.append(URL)
            #print(json.dumps(Race, indent=4))
            #print()

            raceInfo = []
            raceInfo.append(date)
            raceInfo.append(time)
            raceInfo.append(racePlace)
            raceInfo.append(raceName)
            raceInfo.append(race_class)
            raceInfo.append(age)
            raceInfo.append(distance)
            raceInfo.append(None)
            raceInfo.append(None)

            try:
                parseRace(URL, raceInfo, numHorses)
            except:
                pass


