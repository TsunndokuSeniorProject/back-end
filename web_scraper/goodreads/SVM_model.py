import numpy as np
import json

from sklearn.svm import SVC

with open("./train.json", 'r') as fp:
    data = json.load(fp)
    fp.close()


# TODO : tune this fucking noob model 
clf = SVC(gamma='auto')


clf.fit(data["train"], data["class"]) 

with open("./test.json", 'r') as fp:
    data = json.load(fp)
    fp.close()


test = clf.predict(data['test'])


for result, word in zip(test,data['sentence']):
    if result == 1:
        print word
        

print "done"