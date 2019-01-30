import numpy as np
import json
from sklearn.svm import SVC
from sklearn.externals import joblib
import pandas as pd
        
class SVM_subjectivity:
    def __init__(self):
        self.model = SVC(gamma='auto')

    def train(self, x, y):
        self.model.fit(x, y)

    def saveModelState(self):
        filename = 'state/subjectivity_model_state.sav'
        joblib.dump(self.model, filename)

    def loadModelState(self, savePath):
        self.model = joblib.load(savePath)

    def test(self, word_feature, word_map):
        result = self.model.predict(word_feature)
        subjectivity = []
        for ans, wm in zip(result, word_map):
            if ans == 1:
                subjectivity.append(wm)
        return subjectivity
        
if __name__ == "__main__":
    svm = SVM_subjectivity()
#     with open("./train.json", 'r') as fp:
#         data = json.load(fp)
#         fp.close()
#     svm.train(data["train"], data["class"])
#     svm.saveModelState()
    svm.loadModelState('state/subjectivity_model_state.sav')
    wf = [[0.4082482904638631, 1, 4, 0], [0.4082482904638631, 1, 2, 0], [0.4082482904638631, -1, 3, 0], [0.4082482904638631, 1, 2, 0], [0.4082482904638631, -1, 2, 0], [0.4082482904638631, -1, 4, 0]] 
    wm = [u'as', u'fuck', u'is', u'noob', u'shit', u'this']
    print svm.test(wf, wm)