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


print("loading data\n\n")
raw_data = pd.read_excel("hrCut.xlsx")
print("data loaded\n\n")


class Module4_Model:
    
    def __init__(self):
        x = raw_data.iloc[:, :-1].values
        y = raw_data.iloc[:, -1:].values

        imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
        imputer.fit(x[:, 10:])
        x[:, 10:] = imputer.transform(x[:, 10:])


        #error = x[7]

        #dtCount = 0
        #for row in x:
        #  for value in row:
        #    if isinstance(value, datetime.datetime):
        #      dtCount += 1
        #print("{} instances of datetime objects in the data".format(dtCount))




  


        #columnsToBeFixed = [0, 2, 3]
        #originalSize = len(x[0])

        # Increase the size of the table
        #for index in columnsToBeFixed:
        #  z = np.zeros((len(x),1), dtype=int)
        #  x = np.c_[x, z]

        # Sort the values into integers, use the original column for the min and an 
        # extended column for the max figures
        #pos = 0
        #for index in columnsToBeFixed:
        #  for i in range(0, len(x)):
        #    value = x[i][index]
        #    x[i][index] = int(value[:value.find("-")])
        #    x[i][originalSize + pos] = int(value[value.find("-")+1:])
        #  pos += 1


        print("encoding")
        columnsToEncode = [0,1,2]
        ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(), columnsToEncode)], remainder='passthrough')
        tmp = x
        x = np.array(ct.fit_transform(x))
        


        #le = LabelEncoder()
        #y = le.fit_transform(y)

        print("encoding done")

        print(y)

        
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(x, y, test_size = 0.2, random_state = 1)

        
        print(x[0])
        sc = StandardScaler()
        
        self.x_train[:, 18:] = sc.fit_transform(self.x_train[:, 18:])
        
        self.x_test[:, 18:] = sc.transform(self.x_test[:, 18:])
                
    def preprocess_training_data(self):       
        return self.x_train

    def preprocess_test_data(self):
        return self.x_test

    def linear_regression_test(self):
        regressor = LinearRegression()
        regressor.fit(self.x_train, self.y_train)

        y_pred = regressor.predict(self.x_test)
        np.set_printoptions(precision=2)
        results = np.concatenate((y_pred.reshape(len(y_pred),1), self.y_test.reshape(len(self.y_test),1)),1)

        positives = []
        negatives = []

        for result in results:

          if result[1] == 1:
            positives.append(result[0])
          else:
            negatives.append(result[0])

        plt.plot(range(0, len(positives)), positives, color = 'red')
        plt.plot(np.array([0,len(positives)]),np.array([1, 1]), color = 'blue')
        plt.title('Linear Regression POSITIVE CASES')
        plt.ylabel('Estimated chance of repeat occurence')
        plt.show()

        plt.plot(range(0, len(negatives)), negatives, color = 'red')
        plt.plot(np.array([0,len(negatives)]),np.array([0, 0]), color = 'blue')
        plt.plot(np.array([0,len(negatives)]),np.array([1, 1]), color = 'white')
        plt.title('Linear Regression NEGATIVE CASES')
        plt.ylabel('Estimated chance of repeat occurence')
        plt.show()

    def logistic_regression_test(self):
        classifier = LogisticRegression(random_state = 0)
        classifier.fit(self.x_train, self.y_train)
        y_pred = classifier.predict(self.x_test)
        results = np.concatenate((y_pred.reshape(len(y_pred),1), self.y_test.reshape(len(self.y_test),1)),1)

        cm = confusion_matrix(self.y_test, y_pred)
        print(round(accuracy_score(self.y_test, y_pred)*100, 2), "% accuracy")

    def knn_test(self):
        classifier = KNeighborsClassifier(n_neighbors = 5, metric = 'minkowski', p = 2)
        classifier.fit(self.x_train, self.y_train)

        y_pred = classifier.predict(self.x_test)

        cm = confusion_matrix(self.y_test, y_pred)
        print("KNN ",  round(accuracy_score(self.y_test, y_pred)*100, 2), "% accuracy")

    def decision_tree_test(self):
        classifier = DecisionTreeClassifier(criterion = 'entropy', random_state = 0)
        classifier.fit(self.x_train, self.y_train)

        y_pred = classifier.predict(self.x_test)

        cm = confusion_matrix(self.y_test, y_pred)
        #print(cm)
        print("Decision Tree ", round(accuracy_score(self.y_test, y_pred)*100, 2), "% accuracy")

    def svm_test(self):
        classifier = SVC(kernel = 'linear', random_state = 0)
        classifier.fit(self.x_train, self.y_train)

        y_pred = classifier.predict(self.x_test)

        cm = confusion_matrix(self.y_test, y_pred)
        #print(cm)
        print("SVM ", round(accuracy_score(self.y_test, y_pred)*100, 2), "% accuracy")

    def kernel_svm_test(self):
        classifier = SVC(kernel = 'rbf', random_state = 0)
        classifier.fit(self.x_train, self.y_train)

        y_pred = classifier.predict(self.x_test)

        cm = confusion_matrix(self.y_test, y_pred)
        #print(cm)
        print("Kernal SVM ", round(accuracy_score(self.y_test, y_pred)*100, 2), "% accuracy")

    def naive_bayes_test(self):
        classifier = GaussianNB()
        classifier.fit(self.x_train, self.y_train)

        y_pred = classifier.predict(self.x_test)


        cm = confusion_matrix(self.y_test, y_pred)
        #print(cm)
        print("Naive Bayes ", round(accuracy_score(self.y_test, y_pred)*100, 2), "% accuracy")

    def random_forest_test(self):
        classifier = RandomForestClassifier(n_estimators = 15, criterion = 'entropy', random_state = 0)
        classifier.fit(self.x_train, self.y_train)

        y_pred = classifier.predict(self.x_test)

        cm = confusion_matrix(self.y_test, y_pred)
        #print(cm)
        print("Random Forest  ", round(accuracy_score(self.y_test, y_pred)*100, 2), "% accuracy")


    def logistic_regression_test(self):
        classifier = LogisticRegression(random_state = 0)
        classifier.fit(self.x_train, self.y_train)

        y_pred = classifier.predict(self.x_test)
        results = np.concatenate((y_pred.reshape(len(y_pred),1), self.y_test.reshape(len(self.y_test),1)),1)

        cm = confusion_matrix(self.y_test, y_pred)
        #print(cm)
        print("Logistincs regression ", round(accuracy_score(self.y_test, y_pred)*100, 2), "% accuracy")

    def all_tests(self):
        #self.linear_regression_test()
        #self.logistic_regression_test()
        #self.random_forest_test()
        #self.naive_bayes_test()
        #self.kernel_svm_test()
        #self.svm_test()
        #self.knn_test()
        self.decision_tree_test()

my_model = Module4_Model()

x_train_processed = my_model.preprocess_training_data()

x_test_processed = my_model.preprocess_test_data()

my_model.all_tests()







print("done")