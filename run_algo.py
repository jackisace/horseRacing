import pytest
import pandas as pd
import numpy as np
import datetime

#from IPython import embed
import pdb

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

globalwins = 0
globallosses = 0

money = 0
wins = 0
consecutiveLosses = 0
highestConsecutiveLosses = 0
money = 0
wins = 0
losses = 0
streak = 0
highestStreak = 0
money = 0
wins = 0
losses = 0
streak = 0
highestStreak = 0
target = 1
moneyLost = 0
mostMoneyLost = 0
streaks = []
highestConfidence = 0.0

streaks = []
def checkPredictions():
    global globalwins, globallosses
    global money 
    global wins
    global consecutiveLosses 
    global highestConsecutiveLosses 
    global money 
    global wins 
    global losses 
    global streak 
    global highestStreak 
    global money 
    global wins 
    global losses 
    global streak 
    global highestStreak 
    global target 
    global moneyLost 
    global mostMoneyLost 
    global streaks 
    global highestConfidence 
    
    streaks = []
#    pdb.set_trace()
    for r in tomorrowsRaces:
        try:
            highest = None
            highestPrediction = 0.0
            secondHighest = None
            for h in r.horses:
                if h.prediction > highestPrediction:
                    highest = h
                    highestPrediction = h.prediction
                    if highestPrediction > highestConfidence:
                        highestConfidence = highestPrediction
            highestPrediction = 0.0
            for h in r.horses:
                if h is highest:
#                    print("highest found")
                    continue
                if h.prediction > highestPrediction:
                    secondHighest = h
                    highestPrediction = h.prediction
                    if highestPrediction > highestConfidence:
                        highestConfidence = highestPrediction
            

            
            if not highest:
                continue
            if highest.prediction < 0.5:
                continue
            if highest.price > 1:
                continue
            
            target = money + 1

            if highest.position == 1:
                wins += 1
                globalwins += 1
                money = target
                
                if moneyLost > mostMoneyLost:
                    mostMoneyLost = moneyLost
                moneyLost = 0
                consecutiveLosses = 0
                st = "WIN "
            else:
                losses += 1
                globallosses += 1
                consecutiveLosses += 1
                diff = float(target - money)
                diffCost = diff / highest.price
                moneyLost += diffCost
                money -= diffCost
                st = "LOSS"
            print("{} wins:{}    losses:{}    cons:{}    money:{}    pred:{}    2ndP:{}   diff:{}".format(st, wins, losses, consecutiveLosses, money, highest.prediction, second.prediction, (highest.prediction - secondHighest.prediction)))
        except:
            pass

    print("Highest confidence:", highestConfidence)
    print("highest consecutive losses:", highestConsecutiveLosses)
    print("most money lost:", mostMoneyLost)
    print("global wins: {}\tglobal losses: {}".format(globalwins, globallosses))


def checkNewResults(results):
    best = 0
    betOn = None

    for i in range(0, len(results)):
        if results[i] > best:
            best = results[i]
            betOn = i

    if y_pred[betOn][0] == 1:
        print("winner")
    else:
        print("loser")
            

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


        #try:
        Training = True 
        if Training:
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
            ann.fit(x_train, y_train, batch_size = 500, epochs = 20)


            
            with open('ann.pickle', 'wb') as f:
                pickle.dump(ann, f)
        else:
            with open("ann.pickle", "rb") as f:
                ann = pickle.load(f)


        results = ann.predict(x_pred)


        #money = checkResults(results)
        #checkNewResults(results)

        #embed()
        #allMoney.append(money)

        setPredictions(results)
        checkPredictions()
        #except:
        #    pass


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

