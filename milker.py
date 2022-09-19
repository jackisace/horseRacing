
from argparse import _MutuallyExclusiveGroup
from bs4 import BeautifulSoup
import requests
import re
from structure import *
import datetime
import random
import time

currentRaceId = 0
racesMaster = []
horsesMaster = []

def cleanUp(st):
    st = st.replace("  ", "")
    st = st.replace("\n", "")
    while st[-1] == " ":
        st = st[:-1]
    return st

'''urls to test'''

#url = "https://www.racingpost.com/results/36/newbury/2022-09-16/819636"
#url = "https://www.racingpost.com/results/36/newbury/2022-09-16/819634"
#url = 'https://www.racingpost.com/results/36/newbury/2022-09-16/819632'

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-language": "en-GB,en;q=0.9,en-US;q=0.8",
    "sec-ch-ua": "\"Microsoft Edge\";v=\"105\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"105\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1"
  }






def parsePage(racePageHtml):

    soupthisracePage = racePageHtml.text

    open("a.html", "w").write(soupthisracePage)

    soup = BeautifulSoup(soupthisracePage, 'html.parser')
    output = ''
    horses = []
    jockeys = []
    trainers = []
    ages = []
    ors = []
    weights = []
    topspeed = []


    '''Horse names'''
    for thing in soup.find_all('div',class_="rp-horseTable__horse__name"):
        output += ("{}, {}".format(' '.join(thing['class']),thing.text))


    output = "".join(line.strip() for line in output.split("rp-horseTable__horse__name ui-link ui-link_table js-popupLink"))
    output = output.replace('\n', '')
    horses = output.split(',')
    temp = []
    for item in horses:
        if len(item) == 0:
            pass
        else:
            temp.append(item[25:])

    horses = temp


    '''Jockey names'''

    output = ''
    for item in soup.find_all('a',class_=['rp-horseTable__human__link ui-link ui-link_table ui-link_marked ui-profileLink js-popupLink',""]):
        output += ("{}, {}".format(' '.join(item['class']),item.text))


    output = "".join(line.strip() for line in output.split("rp-horseTable__human__link ui-link ui-link_table ui-link_marked ui-profileLink js-popupLink"))
    output = output.replace('\n', '')
    jockeys = output.split(',')
    temp = []
    for item in jockeys:
        if len(item) == 0:
            pass
        else:
            temp.append(item[29:])

    jockeys = temp


    '''Horse Age'''

    output = ''
    for item in soup.find_all('td',class_=['rp-horseTable__spanNarrow rp-horseTable__spanNarrow_age',""]):
        output += ("{}, {}".format(' '.join(item['class']),item.text))


    output = "".join(line.strip() for line in output.split("rp-horseTable__spanNarrow rp-horseTable__spanNarrow_age"))
    output = output.replace('\n', '')
    ages = output.split(',')
    temp = []
    for item in ages:
        if len(item) == 0:
            pass
        else:
            temp.append(item[9:])

    ages = temp


    '''Topsspeed of horse'''


    output = ''
    for item in soup.find_all('td', {'data-test-selector':"full-result-topspeed"}):
        output += ("{}, {}".format(' '.join(item['class']),item.text))


    output = "".join(line.strip() for line in output.split("rp-horseTable__spanNarrow"))
    output = output.replace('\n', '')
    topspeed = output.split(',')
    temp = []
    for item in topspeed:
        if len(item) == 0:
            pass
        else:
            temp.append(item[9:])

    topspeed = temp

    '''Weight -- Still needs to be split by a slash e.g. 810 should be 8/10'''

    output = ''
    for item in soup.find_all('td',class_=['rp-horseTable__spanNarrow rp-horseTable__wgt']):
        output += ("{}, {}".format(' '.join(item['class']),item.text))


    output = "".join(line.strip() for line in output.split("rp-horseTable__spanNarrow rp-horseTable__wgt"))
    output = output.replace('\n', '')
    weights = output.split(',')
    temp = []
    for item in weights:
        if len(item) == 0:
            pass
        else:
            temp.append(item[13:])

    weights = temp

    '''Offical record'''

    output = ''
    for item in soup.find_all('td', {'data-ending':"OR"}):
        output += ("{}, {}".format(' '.join(item['class']),item.text))


    output = "".join(line.strip() for line in output.split("rp-horseTable__spanNarrow"))
    output = output.replace('\n', '')
    ors = output.split(',')
    temp = []
    for item in ors:
        if len(item) == 0:
            pass
        else:
            temp.append(item[9:])
    ors = temp


    '''Trainers names'''
    trainers = []
    for item in soup.find_all('a', {'data-test-selector':"link-trainerName"}):
        a = item.text.replace("\n", "")
        a = a.replace("  ", "")
        trainers.append(a[:-1])
    trainers = list(dict.fromkeys(trainers))


    # class="rp-horseTable__horse__price"
    #print(soup)
    prices = []
    for item in soup.find_all("span", class_="rp-horseTable__horse__price"):
        price = item.text.replace(" ", "")
        price = price.replace("\n", "")
        prices.append(price)

        
    # rp-horseTable__horse__country
    countries = []
    for item in soup.find_all("span", class_="rp-horseTable__horse__country"):
        country = item.text.replace(" ", "")
        country = country.replace("\n", "")
        countries.append(country)


    firstWeights = []
    for item in soup.find_all("span", class_="rp-horseTable__st"):
        weight = item.text.replace(" ", "")
        weight = weight.replace("\n", "")
        firstWeights.append(weight)

    posLengths = []
    for item in soup.find_all("span", class_="rp-horseTable__pos__length"):
        posLength = item.text.replace(" ", "")
        posLength = posLength.replace("\n", "")
        posLengths.append(posLength)

    posLengths = []
    for item in soup.find_all("span", class_="rp-horseTable__pos__length"):
        posLength = item.text.replace(" ", "")
        posLength = posLength.replace("\n", "")
        posLengths.append(posLength)


    pedigrees = []
    for item in soup.find_all("tr", class_="rp-horseTable__pedigreeRow"):
        horsePed = []
        for thing in item.find_all("a", class_="ui-profileLink"):
            horsePed.append(cleanUp(thing.text))
        pedigrees.append(horsePed)




    raceInfo = []

    item = soup.find(class_="rp-raceTimeCourseName__date")
    raceInfo.append(cleanUp(item.text))

    item = soup.find(class_="rp-raceTimeCourseName__time")
    raceInfo.append(item.text)

    item = soup.find(class_="rp-raceTimeCourseName__name")
    raceInfo.append(cleanUp(item.text))

    item = soup.find(class_="rp-raceTimeCourseName__title")
    raceInfo.append(cleanUp(item.text))

    item = soup.find(class_="rp-raceTimeCourseName_class")
    raceInfo.append(cleanUp(item.text))

    item = soup.find(class_="rp-raceTimeCourseName_ratingBandAndAgesAllowed")
    raceInfo.append(cleanUp(item.text))

    item = soup.find(class_="rp-raceTimeCourseName_distance")
    raceInfo.append(cleanUp(item.text))

    item = soup.find(class_="rp-raceTimeCourseName_distanceDetail")
    raceInfo.append(cleanUp(item.text))


    item = soup.find(class_="rp-raceTimeCourseName_condition")
    raceInfo.append(cleanUp(item.text))

    rewards = []
    item = soup.find('div', {'data-test-selector':"text-prizeMoney"})
    for reward in cleanUp(item.text).split("£"):
        r = reward[:-3]
        r = r.replace(",", "")
        rewards.append(r)
    raceInfo.append(rewards[1:])

    RPRs = []
    for item in soup.find_all('td', {'data-ending':"RPR"}):
        RPRs.append(cleanUp(item.text))

    MRs = []
    for item in soup.find_all('td', {'data-ending':"MR"}):
        MRs.append(cleanUp(item.text))


    positions = []
    startingPositions = []

    for item in soup.find_all(class_="rp-horseTable__pos__number"):
        item = cleanUp(item.text)
        position = item[0]
        startingPosition = item[3:].replace(")", "")
        positions.append(position)
        startingPositions.append(startingPosition)




    currentRace = race()
    for i in range(len(horses)):
        thisHorse = horse(  horses[i], 
                            jockeys[i], 
                            trainers[i], 
                            int(ages[i]), 
                            int(topspeed[i]), 
                            int(weights[i]), 
                            int(ors[i]), 
                            prices[i], 
                            countries[i], 
                            firstWeights[i], 
                            posLengths[i],
                            pedigrees[i],
                            positions[i],
                            startingPositions[i],
                            RPRs[i],
                            MRs[i])

    currentRace.print()






datetime_object = datetime.datetime.now()

url = "https://www.racingpost.com/results/DATE"

URLs = []

for i in range(6200): # 6200
    datetime_object = datetime_object - datetime.timedelta(days=1)
    date = (str(datetime_object).split(" ")[0])
    URLs.append(url.replace("DATE", date))


for URL in URLs: # FOR EACH DATE
    print(URL)
    raceURLs = []
    time.sleep(random.randint(0,1))
    urlhtml = requests.get(URL, headers=headers)
    soupthisDate = urlhtml.text
    dateSoup = BeautifulSoup(soupthisDate, 'html.parser')
    
    for item in dateSoup.find_all('a', {'class':"rp-raceCourse__panel__race__info__buttons__link"}): # FOR EACH RACE
        page = str(item).split('href="')[1]
        page = page.split('">')[0]
        raceURLs.append(str("https://www.racingpost.com" + page))

    for race in raceURLs:
        time.sleep(random.randint(0,1))
        raceHtml = requests.get(URL, headers=headers)
        open("a.html", "w").write(raceHtml.text)
        try:
            parsePage(raceHtml)
        except:
            pass


        
