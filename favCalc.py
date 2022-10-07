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
    with open("allRacesNEW.pickle", "rb") as f:
        races = pickle.load(f)
    print("All Data Loaded")



loadAll()

money = 0
wins = 0
losses = 0
streak = 0
highestStreak = 0
target = 1
moneyLost = 0
mostMoneyLost = 0
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

        for h in r.horses:
            if h.price == prices[0]:
                if h.position == 1:
                    wins += 1
                    money = target
                    target += 1
                    if moneyLost > mostMoneyLost:
                        mostMoneyLost = moneyLost
                    moneyLost = 0

                else:
                    losses += 1
                    diff = target - money
                    diffCost = diff / h.price
                    moneyLost += diffCost
                    money -= diffCost

             



        
    except:
        pass
p = 0
for i in streaks:
    p += i


print(mostMoneyLost)    

print(wins, losses, money)
#print("mean streak: " + str(p/len(streaks)))

print(highestStreak)