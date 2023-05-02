import pickle
from structure import horse
import structure
import os
import random

import pandas as pd

files = os.listdir("dataPull/pickles/")
RACES = []
HORSES = []

numHorses = 80000

def loadAll():
    global RACES
    for file in files:
        filename =  "dataPull/pickles/{}".format(file)
        try:
            with open(filename, "rb") as f:
                thisRace = pickle.load(f)
                RACES.append(thisRace)
        except:
            pass

def horseCount():
    horseCount = 0
    for RACE in RACES:
        horseCount += len(RACE.horses)
    print(horseCount, "horses")







def getRace(raceId):
    global files
    for file in files:
        
        if str(raceId) in file:
            filename =  "dataPull/pickles/{}".format(file)
            with open(filename, "rb") as f:
                thisRace = pickle.load(f)
                return thisRace
            

loadAll()
data = []
for R in RACES:
    R.fixData()
    d = R.getData()
    for line in d:
        data.append(line)

df = pd.DataFrame(data)
df.to_csv("final.csv")
#print(df.iloc[:,15:]) 

#loadAll()
#horseCount()