import sklearn
import os
import json
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB, GaussianNB
import re
import csv
from file_reader import file_reader
import random



reviews, labels = file_reader().read_v2("C:/Users/USER/Downloads/test.txt", 1, 2)

train_set = reviews[0:701]
train_labels = labels[0:701]

test_set = reviews[701:750]
test_labels = labels[701:750]
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

count_vec = CountVectorizer()

xtrain = count_vec.fit_transform(train_set)
tfidf_transformer = TfidfTransformer()
xtrain_tfidf = tfidf_transformer.fit_transform(xtrain)

clf = MultinomialNB().fit(xtrain_tfidf, train_labels)
# test_string = ["I hate Harry Potter", "The story is very rich", "Vaguely headachey, I needed a reading distraction, and the appropriate story in these kinds of situations is a touchy one", "The character sucks, I don't enjoy the protagonist at all"]
# test_string.append("Probably the worst part is struggling through all the rampant racism, which isn't nearly as funny as the rampant anti-Mormonism was in aSiS")
# test_string.append("The writing by Agartha Christie is superb, the pacing was great")
# test_string.append("the fact that the cover is the most evocative thing about a novel that should have had atmosphere to die for made me feel like I was dying inside each time I turned the page only to discover 100% plot mechanics and 0% anything of interest besides the, I suppose, \"page-turning\" plot.")
# test_string.append("The emphasis in this well-intentioned advice by Mrs. Fairfax is on the word MARRY.")
# test_string.append("Anna is so bitchy i wanna kill her")
# test_string.append("Is she so terrified of breaking cultural norms and coming across as a mean-crazy-angry-dyke-shrill-frigid bitch")
# test_string.append("How could this be a work of a professional writer? The book was awful to read")
# test = count_vec.transform(test_string)
# test = tfidf_transformer.transform(test)

# with open(test_direc, 'r', encoding='utf-8') as fp:
#     test_data = fp.readlines()
# for sen in test_data:
#     test_set.append(sen)

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
# print(count)