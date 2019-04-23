import sklearn
import os
import json
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB, GaussianNB, ComplementNB
import re
import csv
from model.file_reader import file_reader
import random

# with open(directory, "r", encoding="utf-8") as fp:
#     data = fp.readlines()

# zeros = []
# zero_label = []

raw_review, raw_label = file_reader().read_v2('C:/Users/USER/Downloads/for_pred.txt', 1, 1)

pre_reviews = raw_review[:2200]
pre_labels = raw_label[:2200]
test_set = raw_review[2200:]
test_labels = raw_label[2200:]
count = 0
reviews = []
labels = []
for review, label in zip(pre_reviews, pre_labels):
    if label == 0:
        if count == 3:
            count = 0
            continue
        else:
            count += 1
            reviews.append(review)
            labels.append(label)
    else:
        reviews.append(review)
        labels.append(label)


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

# wtf_zeros = random.sample(zeros, 80)


# ok_labels = []
# for smth in labels:
#     ok_labels.append(smth.replace("\n", "").replace(" ", ""))

# for smth in wtf_zeros:
#     ok_labels.append('0')

# reviews += wtf_zeros
count = {}
for single in labels:
    if single in count:
        count[single] += 1
    else:
        count[single] = 1

print(count)
count_vec = CountVectorizer()

xtrain = count_vec.fit_transform(reviews)
tfidf_transformer = TfidfTransformer()
xtrain_tfidf = tfidf_transformer.fit_transform(xtrain)

clf = ComplementNB().fit(xtrain_tfidf, labels)

# with open(test_direc, 'r', encoding='utf-8') as fp:
#     test_data = fp.readlines()
# for sen in test_data:
#     test_set.append(sen)
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

count = {}
for single in result:
    if single in count:
        count[single] += 1
    else:
        count[single] = 1
print(count)

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
# print(count)