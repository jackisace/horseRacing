from bs4 import BeautifulSoup
import requests
from structure import *
import json


# GET HORSES INFO FROM RACE

def parseRace(url, raceInfo, numHorses):
    print(url)
    response = requests.get(url)
    soupthis = response.text
    soup = BeautifulSoup(soupthis, 'html.parser')

    horses = []
    jockeys = []
    trainers = []
    ages = []
    ors = []
    weights = []
    prices = []

    # OLD VARIABLES - NEED REMOVING
    topspeed = []
    countries = []
    firstWeights = []
    posLengths = []
    pedigrees = []
    positions = []
    startingPositions = []
    RPRs = []
    MRs = []
    forms = []

    horseNames = []
    odds = []
    info = []
    form = []

    horseNum = 0

    for runner in soup.find_all("div",{"data-test-id":"runner"}):

        horseNum += 1

        try:
            horses.append(str(runner.find("a", id="horse-number-{}".format(horseNum)).text).replace("\xa0", " "))
        except:
            horses.append(None)

        try:
            prices.append(runner.find("div", id="horse-odds-{}".format(horseNum)).text)
        except:
            prices.append(None)



        item = runner.find("div",{"data-test-id":"horse-sub-info"})
        info = str(item.text) # Age: 2|  Weight: 9-2|  J: Daniel Muscutt|  T: C & M Johnston|  OR:  90|  D
        infos = info.split("|")
        try:
            ages.append(infos[0].split("Age: ")[1])
        except:
            ages.append(None)
        try:
            weights.append(infos[1].split("Weight: ")[1])
        except:
            weights.append(None)
        try:
            jockeys.append(str(infos[2].split("J: ")[1]).replace("Form:\xa0", ""))
        except:
            jockeys.append(None)
        try:
            trainers.append(str(infos[3].split("T: ")[1]).replace("Form:\xa0", ""))
        except:
            trainers.append(None)
        try:
            ors.append(infos[4].split("OR:  ")[1])
        except:
            ors.append(None)
        topspeed.append(None)
        countries.append(None)
        firstWeights.append(None)
        posLengths.append(None)
        pedigrees.append(None)
        positions.append(None)
        startingPositions.append(None)
        RPRs.append(None)
        MRs.append(None)



        item = runner.find("div",{"data-test-id":"show-form"})
        try:
            forms.append(str(item.text).replace("Form:\xa0", ""))
        except:
            forms.append(None)


    


    currentRace = race(raceInfo, url)
    for i in range(0,horseNum):
        thisHorse = horse(  horses[i], 
                            jockeys[i], 
                            trainers[i], 
                            ages[i], 
                            topspeed[i], 
                            weights[i], 
                            ors[i], 
                            prices[i], 
                            countries[i], 
                            firstWeights[i], 
                            posLengths[i],
                            pedigrees[i],
                            positions[i],
                            startingPositions[i],
                            RPRs[i],
                            MRs[i],
                            forms[i])
    currentRace.saveSL()
    #currentRace.print()


# GET TOMORROWS RACE URLS

url = "https://www.sportinglife.com/racing/racecards/tomorrow"
print(url)
response = requests.get(url)
soupthis = response.text
soup = BeautifulSoup(soupthis, 'html.parser')

a = str(soupthis.split('application/json">')[1])
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

        parseRace(URL, raceInfo, numHorses)
        #input("DONE")


        
#print(urls)