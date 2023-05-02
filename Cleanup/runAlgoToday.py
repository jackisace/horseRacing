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


races = []
originalData = None

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


def checkResults(results):
    global originalData


    for i in range(0, len(results)):
        originalData[i].append(results[i])
        
    output_data = pd.DataFrame(originalData)
    output_data.to_csv("predictions.csv")
    print("predictions.csv created")



    #2022-09-24

tomorrow = "2022-09-24"
print(tomorrow)

races = []
loadAll()
print("Assigning data")
data = []
for race in races:
    race.fixData()
    if tomorrow not in race.date:
        d = race.getData()
        for line in d:
            for i in range(0, len(line)):
                if line[i] == "-":
                    line[i] = None
            data.append(line)
tomorrowsLength = len(data)

for race in races:
    race.fixData()
    if tomorrow in race.date:
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

#y = sc.fit_transform(y)
y_train = y[:tomorrowsLength]
y_pred = y[tomorrowsLength:]



ann = tf.keras.models.Sequential()
ann.add(tf.keras.layers.Dense(units=18, activation="relu"))
ann.add(tf.keras.layers.Dense(units=18, activation="relu"))
ann.add(tf.keras.layers.Dense(units=18, activation="relu"))
ann.add(tf.keras.layers.Dense(units=18, activation="relu"))
ann.add(tf.keras.layers.Dense(units=1, activation="sigmoid"))
ann.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
ann.fit(x_train, y_train, batch_size = 32, epochs = 1)


results = ann.predict(x_pred)



checkResults(results)


