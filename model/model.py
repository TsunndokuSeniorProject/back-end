from sklearn.neighbors import KNeighborsClassifier
from sklearn.externals import joblib
import numpy as np
import pandas as pd

class Model:
    def __init__(self):
        self.model = KNeighborsClassifier(n_neighbors=3)
        self.data = None
        self.X_train = None
        self.Y_train = None

    def prepareData(self, datasetPath):
        self.data = pd.read_csv(datasetPath)
        array = self.data.values
        self.X_train = array[:,1:3]
        self.Y_train = array[:,0]

    def train(self):
        self.model.fit(self.X_train, self.Y_train)

    def saveModelState(self):
        filename = 'state/model_state.sav'
        joblib.dump(self.model, filename)

    def loadModelState(self, savePath):
        self.model = joblib.load(savePath)
        return self.model

    def predict(self, Height, Weight):
        result = self.model.predict([[Height, Weight]])
        print(result)
        return result

if __name__=="__main__":
    knn = Model()
    knn.prepareData('../dataset/person_info.csv')
    knn.train()
    knn.saveModelState()
    knn.predict(155, 60)

