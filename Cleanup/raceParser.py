
from argparse import _MutuallyExclusiveGroup
from bs4 import BeautifulSoup
import requests
import re
from structure import *
import datetime
import random
import time



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






def parsePage(racePageHtml, raceURL):

    soupthisracePage = racePageHtml.text

    if "Sorry, " in soupthisracePage:
        return

    #open("a.html", "w").write(soupthisracePage)

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
    for thing in soup.find_all('a',class_="rp-horseTable__horse__name"):
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
    output = output.replace('  ', '')
    jockeys = output.split(',')
    tmp = []
    jockeys = jockeys[1:]
    for jockey in jockeys:
        try:
            if jockey[0] == " ":
                jockey = jockey[1:]
        except:
            pass

        tmp.append(jockey)


    jockeys = tmp



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

    topspeed = []
    output = ''
    for item in soup.find_all('td', {'data-test-selector':"full-result-topspeed"}):
        topspeed.append(item.text.replace("\n",""))
    for i in range(len(topspeed)):
        if topspeed[i] == "":
            topspeed[i] = "-"


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

    if len(ors) == 0:
        for i in range(len(horses)):
            ors.append("-")


    '''Trainers names'''
    trainers = []
    for item in soup.find_all('a', {'data-test-selector':"link-trainerName"}):
        a = item.text.replace("\n", "")
        a = a.replace("  ", "")
        trainers.append(a[:-1])

    tmp = trainers
    trainers = []
    even = True
    for trainer in tmp:
        if even:
            trainers.append(trainer)
            even = False
        else:
            even = True
    trainers


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
    try:
        raceInfo.append(cleanUp(item.text))
    except:
        raceInfo.append("-")

    item = soup.find(class_="rp-raceTimeCourseName__time")
    try:
        raceInfo.append(item.text)
    except:
        raceInfo.append("-")

    item = soup.find(class_="rp-raceTimeCourseName__name")
    try:
        raceInfo.append(cleanUp(item.text))
    except:
        raceInfo.append("-")

    item = soup.find(class_="rp-raceTimeCourseName__title")
    try:
        raceInfo.append(cleanUp(item.text))
    except:
        raceInfo.append("-")

    item = soup.find(class_="rp-raceTimeCourseName_class")
    try:
        raceInfo.append(cleanUp(item.text))
    except:
        raceInfo.append("-")

    item = soup.find(class_="rp-raceTimeCourseName_ratingBandAndAgesAllowed")
    try:
        raceInfo.append(cleanUp(item.text))
    except:
        raceInfo.append("-")

    item = soup.find(class_="rp-raceTimeCourseName_distance")
    try:
        raceInfo.append(cleanUp(item.text))
    except:
        raceInfo.append("-")

    #not in all pages
    item = soup.find(class_="rp-raceTimeCourseName_distanceDetail")
    try:
        raceInfo.append(cleanUp(item.text))
    except:
        raceInfo.append("-")


    item = soup.find(class_="rp-raceTimeCourseName_condition")
    try:
        raceInfo.append(cleanUp(item.text))
    except:
        raceInfo.append("-")

    rewards = []
    try:
        item = soup.find('div', {'data-test-selector':"text-prizeMoney"})
        for reward in cleanUp(item.text).split("£"):
            r = reward[:-3]
            r = r.replace(",", "")
            rewards.append(r)
        
            raceInfo.append(rewards[1:])
    except:
        raceInfo.append(["-", "-", "-"])

    RPRs = []
    for item in soup.find_all('td', {'data-ending':"RPR"}):
        RPRs.append(cleanUp(item.text))

    if len(RPRs) == 0:
        for i in range(len(horses)):
            RPRs.append("-")

    MRs = []
    for item in soup.find_all('td', {'data-ending':"MR"}):
        MRs.append(cleanUp(item.text))

    if len(MRs) == 0:
        for i in range(len(horses)):
            MRs.append("-")

    positions = []
    startingPositions = []

    for item in soup.find_all(class_="rp-horseTable__pos__number"):
        item = cleanUp(item.text)
        position = item[0]
        startingPosition = item[3:].replace(")", "")
        positions.append(position)
        startingPositions.append(startingPosition)



    
    currentRace = race(raceInfo, raceURL)
    for i in range(len(horses)):
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
                            MRs[i])
    currentRace.save()
    currentRace.print()
    

#url = 'https://www.racingpost.com/results/36/newbury/2022-09-16/819632'

#parsePage(racePageHtml, url)

