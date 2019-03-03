import sklearn
import os
import json
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
import re
reviews = []
labels = []
directory = "C:/Users/USER/Downloads/data.txt"

with open(directory, "r", encoding="utf-8") as fp:
    data = fp.readlines()

for sent in data:
    temp = sent.rsplit(',', 1)
    if temp[1] == ' 0\n':
        continue
    else:
        reviews.append(temp[0])
        labels.append(temp[1])



ok_labels = []
for smth in labels:
    ok_labels.append(smth.replace("\n", "").replace(" ", ""))


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

clf = MultinomialNB().fit(xtrain_tfidf, labels)
test_string = ["I hate Harry Potter", "The story is very rich", "Vaguely headachey, I needed a reading distraction, and the appropriate story in these kinds of situations is a touchy one", "The character sucks, I don't enjoy the protagonist at all"]
test_string.append("Probably the worst part is struggling through all the rampant racism, which isn't nearly as funny as the rampant anti-Mormonism was in aSiS")
test_string.append("The writing by Agartha Christie is superb, the pacing was great")
test_string.append("the fact that the cover is the most evocative thing about a novel that should have had atmosphere to die for made me feel like I was dying inside each time I turned the page only to discover 100% plot mechanics and 0% anything of interest besides the, I suppose, \"page-turning\" plot.")
test_string.append("The emphasis in this well-intentioned advice by Mrs. Fairfax is on the word MARRY.")
test_string.append("Anna is so bitchy i wanna kill her")
test_string.append("Is she so terrified of breaking cultural norms and coming across as a mean-crazy-angry-dyke-shrill-frigid bitch")
test = count_vec.transform(test_string)
test = tfidf_transformer.transform(test)
result = clf.predict(test)
print(result)