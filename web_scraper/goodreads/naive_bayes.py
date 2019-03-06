import sklearn
import os
import json
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
import re
import random
reviews = []
labels = []
directory = "C:/Users/USER/Downloads/1-472.txt"

with open(directory, "r", encoding="utf-8") as fp:
    data = fp.readlines()

zeros = []
zero_label = []

skip = 0
for sent in data:
    if skip == 0:
        skip += 1
        continue
    temp = sent.rsplit(',', 1)
    if temp[1] == ' 0\n':
        zeros.append(temp[0])
        zero_label.append(temp[1])
    else:
        reviews.append(temp[0])
        labels.append(temp[1])

# wtf_zeros = random.sample(zeros, 80)


ok_labels = []
for smth in labels:
    ok_labels.append(smth.replace("\n", "").replace(" ", ""))

# for smth in wtf_zeros:
#     ok_labels.append('0')

# reviews += wtf_zeros
count = {}
for single in ok_labels:
    if single in count:
        count[single] += 1
    else:
        count[single] = 1


print(count)
count_vec = CountVectorizer()
xtrain = count_vec.fit_transform(reviews)
tfidf_transformer = TfidfTransformer()
xtrain_tfidf = tfidf_transformer.fit_transform(xtrain)

clf = MultinomialNB().fit(xtrain_tfidf, ok_labels)
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

test_set = []
test_direc = 'C:/Users/USER/Back-end/sentences_filtered.txt'

with open(test_direc, 'r', encoding='utf-8') as fp:
    test_data = fp.readlines()
for sen in test_data:
    test_set.append(sen)
    if len(test_set) > 1000:
        break

test_X = count_vec.transform(test_set)
test_X = tfidf_transformer.transform(test_X)

result = clf.predict(test_X)
print(result)
ready_for_print = []
a = 0
for single in test_set:
    ready_for_print.append(single+ str(result[a]))
    a+=1
count = {}
for single in result:
    if single in count:
        count[single] += 1
    else:
        count[single] = 1
# with open('bayes_result.txt', 'w', encoding='utf-8') as fp:
#     fp.write(ready_for_print)
# print(ready_for_print)
print(count)