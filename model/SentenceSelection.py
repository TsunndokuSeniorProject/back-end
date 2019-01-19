import os
import json
from sklearn.feature_extraction.text import TfidfVectorizer

tfidf = TfidfVectorizer()
max_chr = 10000
directory = "../web_scraper/novel/comments/"
polar_label = []
review = []
i = 1
for file in os.listdir(directory):
    with open(directory + file, 'r') as fp:
        data = json.load(fp)
        for comment in data['Comment']:
            review.append(comment['Review'])
            i = i + 1
model = tfidf.fit_transform(review)
print(model)
