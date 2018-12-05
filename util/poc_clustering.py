import json
import unidecode
import nltk
import pandas as pd
import os
import sklearn as sk
from sklearn.externals import joblib
from sklearn.cluster import KMeans

model = joblib.load("clustering.sav")
all_sentence = []
save = []
with open("C:/Users/USER/Back-end/dataset/test/review_006246616X.json") as book:
    book = json.load(book)

comments = book['Comment']

for comment in comments:
    for sentence in comment['Review'].split('.'):
        if len(sentence) != 0:
            save.append(sentence)
            row = []
            sum_dict = {}
            sentence = unidecode.unidecode(sentence)
            sentence = sentence
            tokens = nltk.word_tokenize(sentence)
            tagged = nltk.pos_tag(tokens)
            for tagged_word in tagged:
                if "NN" in tagged_word[1] and "NNP" not in tagged_word[1]:
                    sum_dict[tagged_word[0]] = 0
            for tagged_word in tagged:
                if "NN" in tagged_word[1] and "NNP" not in tagged_word[1]:
                    sum_dict[tagged_word[0]] = sum_dict[tagged_word[0]] + 1
                    row.append(tagged_word[0])
            all_sentence.append(sum_dict)
        else:
            continue
df = pd.DataFrame(all_sentence).fillna(value=0, inplace=False)
print(model.predict(df.values))

# result = pd.DataFrame(model.labels_, columns=["Cluster"])
# result = pd.concat([pd.DataFrame(save, columns=["Text"]), result], axis=1)
# result0 = result[result["Cluster"] == 0]
# result0.to_csv("cluster0_result.csv")
# result1 = result[result["Cluster"] == 1]
# result1.to_csv("cluster1_result.csv")
# result2 = result[result["Cluster"] == 2]
# result2.to_csv("cluster2_result.csv")
# result3 = result[result["Cluster"] == 3]
# result3.to_csv("cluster3_result.csv")
# result4 = result[result["Cluster"] == 4]
# result4.to_csv("cluster4_result.csv")
# result5 = result[result["Cluster"] == 5]
# result5.to_csv("cluster5_result.csv")
# result6 = result[result["Cluster"] == 6]
# result6.to_csv("cluster6_result.csv")
# result7 = result[result["Cluster"] == 7]
# result7.to_csv("cluster7_result.csv")

