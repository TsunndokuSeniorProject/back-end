import json
import unidecode
import nltk
import pandas as pd
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')

with open('../web_scraper/novel/comments/review_006246616X.json') as book:

    book = json.load(book)

comments = book['Comment']

# \u2019 = '

all_sentence = []

for comment in comments:
    for sentence in comment['Review'].split('.'):
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
                sum_dict[tagged_word[0]] = sum_dict[tagged_word[0]]+1
                row.append(tagged_word[0])
        all_sentence.append(sum_dict)


df = pd.DataFrame(all_sentence).fillna(value=0, inplace=False)
print df.values