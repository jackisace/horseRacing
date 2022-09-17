# Fixed dependencies - do not remove or change.
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

import matplotlib.pyplot as plt
import tensorflow as tf


print("loading data")
raw_data = pd.read_excel("hr.xlsx")
print("data loaded")


class Module4_Model:
    
    def __init__(self):
        self.x = raw_data.iloc[:, :-1].values
        self.y = raw_data.iloc[:, -1:].values
        print(self.y[0])
        #for i in range(len(self.y)):
        #    if self.y[i] < 4:
        #        self.y[i] = 1.0
        #    else:
        #        self.y[i] = 0.0

        imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
        imputer.fit(self.x[:, 3:])
        self.x[:, 3:] = imputer.transform(self.x[:, 3:])



        
        columnsToEncode = [0,1,2]
        ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(), columnsToEncode)], remainder='passthrough')
        
        self.x = ct.fit_transform(self.x).toarray()
        

        #le = LabelEncoder()
        #
        #y = le.fit_transform(y)

        

        #for i in range(len(y)):
        #    y[i] = float(y[i])
        #

        
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(self.x, self.y, test_size = 0.2, random_state = 1)
        
        

        sc = StandardScaler()
        
        self.x_train = sc.fit_transform(self.x_train)
        
        self.x_test = sc.transform(self.x_test)


    def ann_run(self):
        self.ann = tf.keras.models.Sequential()
        self.ann.add(tf.keras.layers.Dense(units=6, activation="relu"))
        self.ann.add(tf.keras.layers.Dense(units=6, activation="relu"))
        self.ann.add(tf.keras.layers.Dense(units=1, activation="sigmoid"))
        self.ann.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
        self.ann.fit(self.x_train, self.y_train, batch_size = 32, epochs = 200)




my_model = Module4_Model()



my_model.ann_run()







print("done")