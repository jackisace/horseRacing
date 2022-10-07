from bs4 import BeautifulSoup
import requests
import datetime
import time
import json

from structure import *



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

    i = 0

    for runner in soup.find_all("div",{"data-test-id":"runner"}):

        i += 1

        try:
            horses.append(str(runner.find("a", id="horse-number-{}".format(i)).text).replace("\xa0", " "))
        except:
            horses.append(None)

        try:
            prices.append(runner.find("div", id="horse-odds-{}".format(i)).text)
        except:
            prices.append(None)

        try:
            positions.append(runner.find("div",{"data-test-id":"position-no"}))
        except:
            positions.append(None)




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
        #positions.append(None)
        startingPositions.append(None)
        RPRs.append(None)
        MRs.append(None)



        item = runner.find("div",{"data-test-id":"show-form"})
        try:
            forms.append(str(item.text).replace("Form:\xa0", ""))
        except:
            forms.append(None)


    


    currentRace = race(raceInfo, url)
    for i in range(0,numHorses):
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





#datetime_object = datetime.datetime.now()
datetime_object = datetime.datetime(2022, 9, 25) # YYYY, MM, DD

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
    #url = "https://www.sportinglife.com/racing/results/DATE/PLACE/RACEID/NAME"
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
                print("FAILED: " + URL)

