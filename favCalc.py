#import pytest
import pandas as pd
import numpy as np
#import datetime

#from sklearn.preprocessing import LabelEncoder, OneHotEncoder
#from sklearn.compose import ColumnTransformer
#from sklearn.model_selection import train_test_split
#from sklearn.preprocessing import StandardScaler
#from sklearn.linear_model import LinearRegression, LogisticRegression
#from sklearn.naive_bayes import GaussianNB
#from sklearn.svm import SVC
#from sklearn.neighbors import KNeighborsClassifier
#from sklearn.ensemble import RandomForestClassifier
#from sklearn.tree import DecisionTreeClassifier
#from sklearn.metrics import confusion_matrix, accuracy_score
#from sklearn.impute import SimpleImputer
import pickle
from structure import *
import structure
import os
#import random

import pandas as pd

#import matplotlib.pyplot as plt
#import tensorflow as tf


races = []
originalData = None

def loadAll():
    print("Loading All Data")
    global races
    races = []
    with open("allRaces.pickle", "rb") as f:
        races = pickle.load(f)
    print("All Data Loaded")



loadAll()

money = 0
wins = 0
losses = 0
streak = 0
highestStreak = 0
streaks = []
for r in races:

    try:
        r.getData()    
        #if r.date == '2022-06-17':
        prices = []
        bettingHorses = []
        mNumHorses = len(r.horses)
        favHorse = None
        ffavHorse = None
        fffavHorse = None

        for h in r.horses:
            try:
                prices.append(h.price)
            except:
                pass
        
        prices.sort()

        #for i in range(len(r.horses)):
        #    if i > 4:
        #        for h in r.horses:
        #            if h not in bettingHorses:
        #                if prices[i] == h.price:
        #                    bettingHorses.append(h)

        for fHorse in bettingHorses:
            if fHorse.position == 1:
                print(r.raceURL, fHorse.name, fHorse.price, fHorse.position)
                money += fHorse.price
                wins += 1
                if streak > highestStreak:
                    highestStreak = streak
                streaks.append(streak)
                streak = 0
            else:
                money -= 1
                losses += 1
                streak += 1
            print(wins, losses, money)
    except:
        pass
p = 0
for i in streaks:
    p += i

print(wins, losses, money)
print("mean streak: " + str(p/len(streaks)))

print(highestStreak)