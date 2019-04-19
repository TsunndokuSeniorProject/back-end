import sklearn
import os
import json
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB, GaussianNB, ComplementNB
import re
import csv
from file_reader import file_reader
import random


# with open("C:/Users/USER/Downloads/sentence-polarity/sentence_polarity/rt-polarity-pos.txt", 'r', encoding='utf8') as fp:
#     pos = fp.readlines()
# pos_label = [ 1 for x in pos]
# with open("C:/Users/USER/Downloads/sentence-polarity/sentence_polarity/rt-polarity-neg.txt", 'r', encoding='utf8') as fp:
#     neg = fp.readlines()
# neg_label = [ 2 for x in pos]

# train_set = pos + neg
# train_labels = pos_label + neg_label

reviews, labels = file_reader().read_v2("C:/Users/USER/Downloads/test.txt", 2, 2)
print(labels)
train_set = []
train_labels = []
X_reviews = reviews[:1600]
X_labels = labels[:1600]

count = 0
for x, y in zip(X_reviews, X_labels):
    if y in [0,4,5,6]:
        continue
    elif y == 1:
        if count == 5:
            count = 0
            continue
        else:
            count += 1
            train_set.append(x)
            train_labels.append(y)
    else:
        train_set.append(x)
        train_labels.append(y)

raw_test_set = reviews[1601:]
raw_test_labels = labels[1601:]
# with open(directory, "r", encoding="utf-8") as fp:
#     data = fp.readlines()

# zeros = []
# zero_label = []

# with open("C:/Users/USER/Downloads/test.txt") as fp:
#     data = fp.readlines()
# fp.close()

# skip = 0
# for sent in data:
#     if skip == 0:
#         skip += 1
#         continue
#     temp = sent.rsplit(',', 1)
#     if temp[1] == ' 0\n':
#         zeros.append(temp[0])
#         zero_label.append(temp[1])
#     else:
#         reviews.append(temp[0])
#         labels.append(temp[1])

count = {}
for single in train_labels:
    if single in count:
        count[single] += 1
    else:
        count[single] = 1
print(count)
count_vec = CountVectorizer()

xtrain = count_vec.fit_transform(train_set)
tfidf_transformer = TfidfTransformer()
xtrain_tfidf = tfidf_transformer.fit_transform(xtrain)

clf = ComplementNB().fit(xtrain_tfidf, train_labels)


# test
# raw_test_set, raw_test_labels = file_reader().read_v2("C:/Users/USER/Downloads/test.txt", 1, 2)
test_set = []
test_labels = []
for a, b in zip(raw_test_set, raw_test_labels):
    if b == 0:
        continue
    else:
        test_set.append(a)
        test_labels.append(b)
    # test_set.append(a)
    # test_labels.append(b)

count = {}
for single in test_labels:
    if single in count:
        count[single] += 1
    else:
        count[single] = 1
print(count)




test_X = count_vec.transform(test_set)
test_X = tfidf_transformer.transform(test_X)
right = 0
whole = 0
result = clf.predict(test_X)
curr = 0
for each, res in zip(test_labels, result):
    # if test_labels[curr] == result[curr]:
    #     right += 1
    #     whole += 1
    # else:
    #     whole += 1
    if each == res:
        curr+=1

print(curr*100.0/len(result))
ready_for_print = ""
a = 0
for single in test_set:
    ready_for_print = ready_for_print + single + ", " + str(result[a])
    a+=1
count = {}
for single in result:
    if single in count:
        count[single] += 1
    else:
        count[single] = 1
# with open('bayes_result.txt', 'w', encoding='utf-8') as fp:
#     fp.write(ready_for_print)
print(count)