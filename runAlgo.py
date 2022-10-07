import pytest
import pandas as pd
import numpy as np
import datetime

from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.impute import SimpleImputer
import pickle
from structure import *
import structure
import os
import random

import pandas as pd

#import matplotlib.pyplot as plt
import tensorflow as tf

tomorrowsRaces = []
races = []
originalData = None
tomorrow = None

def loadAll():
    print("Loading All Data")
    global races
    races = []
    with open("allRacesNEW.pickle", "rb") as f:
        races = pickle.load(f)
    print("All Data Loaded")

def horseCount():
    loadAll()
    horseCount = 0
    global races
    for race in races:
        horseCount += len(race.horses)
    print(horseCount, "horses")

def getRace(raceId):
    files = os.listdir("pickles/")
    for file in files:
        
        if str(raceId) in file:
            filename =  "pickles/{}".format(file)
            with open(filename, "rb") as f:
                thisRace = pickle.load(f)
                return thisRace

def setPredictions(results):
    i = 0
    for r in tomorrowsRaces:
        for h in r.horses:
            h.prediction = float(results[i][0])
            i += 1   

def checkPredictions():
    money = 0
    wins = 0
    consecutiveLosses = 0
    highestConsecutiveLosses = 0
    for r in tomorrowsRaces:
        highest = None
        highestPrediction = 0.0
        for h in r.horses:
            if h.prediction > highestPrediction:
                highest = h
                highestPrediction = h.prediction
        
        if highest.position == 1:
            money += highest.price
            wins += 1
            
            if consecutiveLosses > highestConsecutiveLosses:
                highestConsecutiveLosses = consecutiveLosses
            consecutiveLosses = 0
        else:
            money -= 1
            consecutiveLosses += 1
            
        print(wins, consecutiveLosses, money)
    print("highest consecutive losses:", highestConsecutiveLosses)



            

def checkResults(results):
    global originalData
    mon = []
    for j in range(20,70):
        j /= 100
        wins = 0
        fails = 0
        moneyMade = 0
        moneyLost = 0
        money = 0
        bets = 0
        for i in range(0, len(results)):
            if results[i] > j:
                bets += 1
                #print(originalData[i][9], results[i], y_pred[i])
                #if y_pred[i][0] == 0:
                #    fails += 1
                #    money -= 1
                    #print("lose", money)
                if y_pred[i][0] == 1:
                    wins += 1
                    try:
                        money += float(originalData[i][-7])
                        #print(float(originalData[i][-4]))
                    
                    except:
                        pass
                else:
                    fails += 1
                    money -= 1
                    #print("win", money)
        print("confidence:", j, "bets:", bets, "money:", money)#, fails/wins)
        mon.append(money)
    return mon
#print(moneyMade, moneyLost)


allMoney = []

for month in range(6,8):
    for day in range(1,28):

    #2022-09-24
        
        tomorrow = "2022-{:02d}-{:02d}".format(month, day)
        print(tomorrow)

        races = []
        loadAll()
        print("Assigning data")
        data = []
        tomorrowsRaces = []        

        for race in races:
            race.fixData()
            if tomorrow not in race.date:
                d = race.getData()
                for line in d:
                    for i in range(0, len(line)):
                        if line[i] == "-":
                            line[i] = None
                    data.append(line)
            else:
                tomorrowsRaces.append(race)
        tomorrowsLength = len(data)
        
        for race in tomorrowsRaces:
            d = race.getData()
            for line in d:
                for i in range(0, len(line)):
                    if line[i] == "-":
                        line[i] = None
                data.append(line)
        print("Data assigned")

        print(tomorrowsLength)
        print(len(data))

        raw_data = pd.DataFrame(data)
        originalData = data[tomorrowsLength:]
        raw_data.to_csv("final.csv")
        print("final.csv created")

        raw_data = pd.DataFrame(data)

        columnsToEncode = [0, 2, 3, 4, 5, 6, 8]
        le = LabelEncoder()
        for column in columnsToEncode:
            first_col = raw_data.pop(column)
            first_col = le.fit_transform(first_col)
            raw_data.insert(0, column,first_col)

        #raw_data.to_csv("finalCheck.csv")


        x = raw_data.iloc[:, :-1].values
        y = raw_data.iloc[:, -1:].values

        for i in range(len(y)):
            try:
                if y[i] < 2:
                    y[i] = 1.0
                else:
                    y[i] = 0.0
            except:
                y[i] = 0.0


        imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
        imputer.fit(x)
        x = imputer.transform(x)



        #x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = todaysLength)
        #originalXTest = x_test

        #todaysLength

        sc = StandardScaler()
        #x_train = sc.fit_transform(x_train)
        #x_test = sc.transform(x_test)

        x = sc.fit_transform(x)
        x_train = x[:tomorrowsLength]
        x_pred = x[tomorrowsLength:]

        #y = sc.transform(y)
        y_train = y[:tomorrowsLength]
        y_pred = y[tomorrowsLength:]


        try:

            ann = tf.keras.models.Sequential()
            ann.add(tf.keras.layers.Dense(units=40, activation="relu"))
            ann.add(tf.keras.layers.Dense(units=40, activation="relu"))
            ann.add(tf.keras.layers.Dense(units=40, activation="relu"))
            ann.add(tf.keras.layers.Dense(units=40, activation="relu"))
            ann.add(tf.keras.layers.Dense(units=40, activation="relu"))
            ann.add(tf.keras.layers.Dense(units=40, activation="relu"))
            ann.add(tf.keras.layers.Dense(units=40, activation="relu"))
            ann.add(tf.keras.layers.Dense(units=40, activation="relu"))
            ann.add(tf.keras.layers.Dense(units=1, activation="sigmoid"))
            ann.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
            ann.fit(x_train, y_train, batch_size = 500, epochs = 10)


            results = ann.predict(x_pred)



            money = checkResults(results)

            allMoney.append(money)

            setPredictions(results)
            checkPredictions()
        except:
            pass


zpone = 0
zptwo = 0
zpthree = 0

for day in allMoney:
    zpone += day[0]
    zptwo += day[1]
    zpthree += day[2]

print("zpone",zpone)
print("zptwo",zptwo)
print("zpthree",zpthree)

