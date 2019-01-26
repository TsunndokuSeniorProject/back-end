# tf idf
# position
# POS
# seed word {pos_adj} {neg_adj}
# negation : not infront of [adv]? adj
# modifier : [adv]? adj

import numpy as np
import os
import json
import re
import string
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk import word_tokenize
from nltk.stem.porter import PorterStemmer


def tokenize(text):
    tokens = word_tokenize(text)
    return do_stem(tokens)

def do_stem(word_list):
    stems = []
    for item in word_list:
        stems.append(PorterStemmer().stem(item))
    return stems

directory = "./novel/crime/"
books = [name for name in os.listdir(directory)]

# read all comments

text = ""

for book in books:
    with open(directory+book, 'r') as fp:
        data = json.load(fp)
        fp.close()
    for review in data['Reviews']:
        text = text + review['Review'] + " "
    


negation_words = ["imperfect","impossible","inelegant","insane","misunderstood","unfair","unfavorable","unhappy","unhealthy","unjust","unlucky","unpleasant","unsatisfactory","unsightly","untoward","unwanted","unwelcome","unwholesome","unwieldy","unwise","worthless","never","neigther","nobody","no","none","nor","nothing","nowhere","not","n't"]

corpus = ['foul', 'elegant', 'gargantuan', 'hot', 'predictable', 'amusing', 'best', 'gritty', 'unique', 'memorable', 'respectable', 'happy', 'understandable', 'nicest', 'brilliant', 'positive', 'angry', 'awesome', 'ridiculous', 'sad', 'prime', 'worried', 'unlikeable', 'favorite', 'unreliable', 'forgettable', 'corniest', 'sucked', 'unsettling', 'cryptic', 'reliable', 'funny', 'curious', 'appropriate', 'considerable', 'incomplete', 'concerned', 'excessive', 'anxious', 'great', 'perfect', 'legendary', 'pompous', 'delightful', 'enigmatic', 'monumental', 'empathetic', 'hilarious', 'scary', 'scare', 'staggered', 'crappy', 'painful', 'awed', 'misogynistic', 'hypocrite', 'trivial', 'catastrophic', 'pretentious', 'unspeakable', 'magnetic', 'controversial', 'appreciate', 'shameful', 'flawless', 'unremorseful', 'grave', 'preferred', 'nasty', 'horrendous', 'petty', 'selfless', 'phenomenal', 'adorable', 'emotional', 'interested', 'unwilling', 'grateful', 'distasteful', 'enjoyable', 'unlovable', 'unimpressive', 'intrigued', 'attached', 'explosive', 'valuable', 'spectacular', 'superfluous', 'unputdownable', 'dreadful', 'inspired', 'underwhelming', 'terrible', 'sensual', 'superior', 'lit', 'pretty', 'horrid', 'uncanny', 'disruptive', 'marvelous', 'nonsense', 'amateurish', 'dull', 'virtuous', 'wonderful', 'fearsome', 'wondrous', 'keen', 'powerful', 'cartoonish', 'unadulterated', 'awe', 'prickly', 'horrible', 'fantastic', 'unforgettable', 'yucky', 'annoyed', 'bad', 'unenlightened', 'unpleasant', 'captivated', 'enjoyable', 'exotic', 'cheesy', 'gripped', 'grim', 'notable', 'despicable', 'romantic', 'deep', 'gaslight', 'vile', 'hideous', 'favourable', 'disastrous', 'unbearable', 'sharp', 'lousy', 'exquisite', 'pathetic', 'pleasant', 'extraordinary', 'laughable', 'insightful', 'insufferable', 'significant', 'unenjoyable', 'cynical', 'fun', 'foolish', 'humorous', 'underdeveloped', 'epic', 'agreeable', 'lame', 'finest', 'comfortable', 'absurd', 'remorseful', 'exceptional', 'glorious', 'tremendous', 'frustrating', 'likable', 'marketable', 'excellent', 'hypnotic', 'marvellous', 'lovable', 'euphoric', 'questionable', 'heinous', 'remarkable', 'impressive', 'unbelievable', 'hurtful', 'ideal', 'untrustworthy', 'good', 'awful', 'outstanding', 'cleverly', 'distinctive', 'likeable', 'unendurable', 'intense', 'impressed', 'smitten', 'understatement', 'impatient', 'unforgivable', 'untouchable', 'shallow', 'asshole', 'typical', 'utter', 'inventive', 'masterful', 'decent', 'wild', 'attractive', 'rare', 'unlikable', 'sick', 'frustrate']


# preprocess text data

text = re.sub(r'[^\x00-\x7F]+','', text)

text = text.lower().replace(".", "").replace("-"," ").replace("_"," ").replace("/","")

text = re.sub(r'\d+', '', text)

text = re.split('\.|\?|\!',text)





# convert all negation word into its root word

negation_words = do_stem(negation_words)

# convert all corpus word into its root word

corpus = do_stem(corpus)

# convert a

text = [" ".join(tokenize(txt.lower())) for txt in text]

vectorizer = TfidfVectorizer()
matrix = vectorizer.fit_transform(text).todense()
matrix = pd.DataFrame(matrix, columns=vectorizer.get_feature_names())
top_words = matrix.sum(axis=0).sort_values(ascending=False)
token = list(matrix.keys())
index = 0

word_feature = []
label = []
mapp = []
for sentence in text:
    for word in token:
        if word in sentence:
            
            position = sentence.index(word)
            mid_sentence_len = len(sentence)/2
            if position > mid_sentence_len:
                position = 1
            elif position == mid_sentence_len:
                position = 0
            else:
                position = -1

            POS = nltk.pos_tag([word])
            if "JJ" in str(POS[0][1]):
                POS = 0
            elif "RB" in str(POS[0][1]):
                POS = 1
            elif "NN" in str(POS[0][1]):
                POS = 2
            elif "VB" in str(POS[0][1]):
                POS = 3
            else:
                POS = 4

            nega = 0
            if word in negation_words:
                nega = 1

            isSeed = 0
            if word in corpus:
                isSeed = 1
                # print "TFIDF : "+str(matrix[word].loc[index])+" Seed : "+str(isSeed)+" position : "+str(position)+" POS : "+str(POS[0][1])+" Negation : "+str(nega)

            word_feature.append([matrix[word].loc[index], position, POS, nega])
            
            # to create a training set collect isSeed variable otherwise word
            label.append(isSeed)
            mapp.append(word)
    index += 1

with open("./train.json", 'w+') as fp:
    json.dump({
        "train":word_feature,
        "class":label
    },fp)
    fp.close()

with open("./test.json", 'w+') as fp:
    json.dump({
        "test":word_feature,
        "sentence":mapp
    },fp)
    fp.close()


