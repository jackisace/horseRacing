
from argparse import _MutuallyExclusiveGroup
from bs4 import BeautifulSoup
import requests
import re
from structure import *
import datetime
import random
import time




def cleanUp(st):
    st = st.replace("T:\xa0", "")
    st = st.replace("\n", "")
    while st[0] == " ":
        st = st[1:]
    while st[-1] == " ":
        st = st[:-1]
    return st



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
    for thing in soup.find_all('a',class_="RC-runnerName"):
        horses.append(cleanUp(thing.text))

    


    '''Jockey names'''

    output = ''
    for item in soup.find_all('a',class_=['RC-runnerInfo_jockey',""]):
        jockeys.append(cleanUp(item.text))




    '''Horse Age'''

    output = ''
    for item in soup.find_all('span',class_=['RC-runnerAge',""]):
        ages.append(cleanUp(item.text))



    '''Topsspeed of horse'''

    topspeed = []
    output = ''
    for item in soup.find_all('span',class_=['RC-runnerTs',""]):
        topspeed.append(cleanUp(item.text))
    for i in range(len(topspeed)):
        if topspeed[i] == "":
            topspeed[i] = None


    '''Weight -- Still needs to be split by a slash e.g. 810 should be 8/10'''

    for item in soup.find_all('span',class_=['RC-runnerWgt__carried']):
        weights.append(cleanUp(item.text))


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
            ors.append(None)


    '''Trainers names'''
    trainers = []
    for item in soup.find_all('a', {'data-test-selector':"RC-cardPage-runnerTrainer-name"}):
        trainers.append(cleanUp(item.text))

    countries = []
    for item in trainers:
        countries.append(None)



    firstWeights = []
    for item in soup.find_all("span", class_="RC-runnerWgt__carried_st"):
        firstWeights.append(cleanUp(item.text))

#
    posLengths = []
    for item in trainers:
        posLengths.append(None)



    pedigrees = []
    for item in trainers:
        pedigrees.append([None, None, None])



    raceInfo = []
    item = soup.find(class_="RC-courseHeader__date")
    try:
        raceInfo.append(cleanUp(item.text))
    except:
        raceInfo.append(None)

    item = soup.find(class_="RC-courseHeader__time")
    try:
        raceInfo.append(cleanUp(item.text))
    except:
        raceInfo.append(None)

    item = soup.find(class_="RC-courseHeader__nameLink")
    try:
        raceInfo.append(cleanUp(item.text))
    except:
        raceInfo.append(None)

    item = soup.find('span', {'data-test-selector':"RC-header__raceInstanceTitle"})
    try:
        raceInfo.append(cleanUp(item.text))
    except:
        raceInfo.append(None)

    item = soup.find('span', {'data-test-selector':"RC-header__raceClass"})
    try:
        raceInfo.append(cleanUp(item.text))
    except:
        raceInfo.append(None)

    item = soup.find('span', {'data-test-selector':"RC-header__rpAges"})
    try:
        raceInfo.append(cleanUp(item.text))
    except:
        raceInfo.append(None)

    item = soup.find(class_="RC-cardHeader__distance")
    try:
        raceInfo.append(cleanUp(item.text))
    except:
        raceInfo.append(None)

    item = soup.find(class_="rp-raceTimeCourseName_distanceDetail") # CANT GET FOR FUTURE RACES
    try:
        raceInfo.append(cleanUp(item.text))
    except:
        raceInfo.append(None)


    item = soup.find(class_="rp-raceTimeCourseName_condition") # CANT GET FOR FUTURE RACES
    try:
        raceInfo.append(cleanUp(item.text))
    except:
        raceInfo.append(None)

    rewards = []
    try:
        item = soup.find('div', {'data-test-selector':"text-prizeMoney"})
        for reward in cleanUp(item.text).split("£"):
            r = reward[:-3]
            r = r.replace(",", "")
            rewards.append(r)
            raceInfo.append(rewards[1:])
    except:
        raceInfo.append([None, None, None])

    RPRs = []
    for item in soup.find_all('span', 'RC-runnerRpr'):
        RPRs.append(cleanUp(item.text))

    if len(RPRs) == 0:
        for i in range(len(horses)):
            RPRs.append(None)

    MRs = []
    for item in soup.find_all('td', {'data-ending':"MR"}):
        MRs.append(cleanUp(item.text))

    if len(MRs) == 0:
        for i in range(len(horses)):
            MRs.append(None)

    positions = []
    startingPositions = []

    for item in horses:
        positions.append(None)
        startingPositions.append(None)

    
    prices = []
    for i in range(len(horses)):

        price = input(horses[i] + ": ")
        prices.append(str(price))




    
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
    #currentRace.print()
    





