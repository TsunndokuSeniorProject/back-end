import sklearn
import os
import json
from sklearn.feature_extraction.text import CountVectorizer
import re
reviews = []
labels = []
directory = "C:/Users/USER/Downloads/data.txt"

with open(directory, "r", encoding="utf-8") as fp:
    data = fp.readlines()

for sent in data:
    temp = sent.rsplit(',', 1)
    reviews.append(temp[0])
    labels.append(temp[1])


print(reviews)
print(labels)

# count_vec = CountVectorizer()
# count_vec.fit