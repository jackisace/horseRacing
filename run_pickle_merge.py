import pickle
import os


races = []

def loadMain():
    global races
    races = []
    with open("allRacesNEW.pickle", "rb") as f:
        races = pickle.load(f)


def addNewPickles():
    files = os.listdir("pickles/")
    for file in files:
        filename =  "pickles/{}".format(file)
        with open(filename, "rb") as f:
            thisRace = pickle.load(f)
        races.append(thisRace)

def countRaces():
    print("number of races: {}".format(len(races)))


def saveRaces():
    filename = "allRaces1.pickle"
    with open(filename, 'wb') as f:
        pickle.dump(races, f)


loadMain()
countRaces()

addNewPickles()
countRaces()

saveRaces()

