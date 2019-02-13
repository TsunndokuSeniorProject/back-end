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
    return tokens

def do_stem(word_list):

    stems = []
    for item in word_list:
        stems.append(PorterStemmer().stem(item))
    return stems

directory = "./novel/romance/"
books = [name for name in os.listdir(directory)]

# read all comments

text = ""

for book in books:
    if book != ".DS_Store":
        with open(directory+book, 'r') as fp:
            data = json.load(fp)
            fp.close()
        for review in data['Reviews']:
            text = text + review['Review'] + " "

negation_words = ["imperfect","impossible","inelegant","insane","misunderstood","unfair","unfavorable","unhappy","unhealthy","unjust","unlucky","unpleasant","unsatisfactory","unsightly","untoward","unwanted","unwelcome","unwholesome","unwieldy","unwise","worthless","never","neigther","nobody","no","none","nor","nothing","nowhere","not","n't"]

# corpus = ['foul', 'elegant', 'gargantuan', 'hot', 'predictable', 'amusing', 'best', 'gritty', 'unique', 'memorable', 'respectable', 'happy', 'understandable', 'nicest', 'brilliant', 'positive', 'angry', 'awesome', 'ridiculous', 'sad', 'prime', 'worried', 'unlikeable', 'favorite', 'unreliable', 'forgettable', 'corniest', 'sucked', 'unsettling', 'cryptic', 'reliable', 'funny', 'curious', 'appropriate', 'considerable', 'incomplete', 'concerned', 'excessive', 'anxious', 'great', 'perfect', 'legendary', 'pompous', 'delightful', 'enigmatic', 'monumental', 'empathetic', 'hilarious', 'scary', 'scare', 'staggered', 'crappy', 'painful', 'awed', 'misogynistic', 'hypocrite', 'trivial', 'catastrophic', 'pretentious', 'unspeakable', 'magnetic', 'controversial', 'appreciate', 'shameful', 'flawless', 'unremorseful', 'grave', 'preferred', 'nasty', 'horrendous', 'petty', 'selfless', 'phenomenal', 'adorable', 'emotional', 'interested', 'unwilling', 'grateful', 'distasteful', 'enjoyable', 'unlovable', 'unimpressive', 'intrigued', 'attached', 'explosive', 'valuable', 'spectacular', 'superfluous', 'unputdownable', 'dreadful', 'inspired', 'underwhelming', 'terrible', 'sensual', 'superior', 'lit', 'pretty', 'horrid', 'uncanny', 'disruptive', 'marvelous', 'nonsense', 'amateurish', 'dull', 'virtuous', 'wonderful', 'fearsome', 'wondrous', 'keen', 'powerful', 'cartoonish', 'unadulterated', 'awe', 'prickly', 'horrible', 'fantastic', 'unforgettable', 'yucky', 'annoyed', 'bad', 'unenlightened', 'unpleasant', 'captivated', 'enjoyable', 'exotic', 'cheesy', 'gripped', 'grim', 'notable', 'despicable', 'romantic', 'deep', 'gaslight', 'vile', 'hideous', 'favourable', 'disastrous', 'unbearable', 'sharp', 'lousy', 'exquisite', 'pathetic', 'pleasant', 'extraordinary', 'laughable', 'insightful', 'insufferable', 'significant', 'unenjoyable', 'cynical', 'fun', 'foolish', 'humorous', 'underdeveloped', 'epic', 'agreeable', 'lame', 'finest', 'comfortable', 'absurd', 'remorseful', 'exceptional', 'glorious', 'tremendous', 'frustrating', 'likable', 'marketable', 'excellent', 'hypnotic', 'marvellous', 'lovable', 'euphoric', 'questionable', 'heinous', 'remarkable', 'impressive', 'unbelievable', 'hurtful', 'ideal', 'untrustworthy', 'good', 'awful', 'outstanding', 'cleverly', 'distinctive', 'likeable', 'unendurable', 'intense', 'impressed', 'smitten', 'understatement', 'impatient', 'unforgivable', 'untouchable', 'shallow', 'asshole', 'typical', 'utter', 'inventive', 'masterful', 'decent', 'wild', 'attractive', 'rare', 'unlikable', 'sick', 'frustrate']
corpus = ['disappointed', 'strong', 'light-years', 'satisfied', 'grand', 'popular', 'magical', 'poor', 'love', 'stupid', 'beautiful', 'favourite', 'beloved', 'crazy', 'admirable', 'brainless', 'classic', 'spirited', 'bold', 'amazing', 'silly', 'profound', 'sophisticated', 'neglected', 'Good', 'enjoyed', 'connected', 'offending', 'fucking', 'atrocious', 'original', 'trash', 'damn', 'ludicrous', 'well-written', 'interesting', 'well-researched', 'trashy', 'soul-reaching', 'gut-wrenching', 'freaking', 'LOVELY', 'tasteful', '5-stars', 'pleased', 'over-the-top', 'biased', 'heartbroken', 'anti-climactic', 'outlandish', 'half-assed', 'corny', 'climactic', 'miserable', 'tense', 'upsetting', 'yawn-worthy', 'imperfect', 'gross', 'oh-so-wonderful', 'frightening', 'joyful', 'heartbreaking', 'eye-opening', 'excited', 'utterly', 'disappointing', 'shitty', 'heart-wrenching', 'clever', 'tragic', 'uncomfortable', 'lovely', 'soul-squeezing', 'disbelieving', 'boring', 'inconclusive', 'irritating', 'inspirational', 'hooked', 'hate', 'entertaining', 'annoying', 'badass', 'depressing', 'dry', 'rip-roaring', 'earth-shattering', 'vulnerable', 'jaw-dropping', 'tedious', 'mind-numbing', 'enjoy', 'charming', 'compelling', 'thrilled', 'kick-ass', 'appalling', 'unimaginative', 'Brilliant', 'generic', 'irritable', 'thought-provoking', 'fabulous', 'page-turning', 'gripping', 'captivating', 'overwhelming', 'engaging', 'Unputdownable', 'Wonderful', 'impeccable', 'heartwarming', 'satisfying', 'heart-stirring', 'talented', 'creepy', 'subpar', 'awkward', 'stellar', 'cringe', 'mind-fuck', 'savage', 'speechless', 'unpredictable', 'visceral', 'mediocre', 'meaningful', 'worthless', 'choppy', 'butterfly-inducing', 'Stuff-of-dreams', 'panty-dropping', 'touching', 'underwhelmed', 'Pathetic', 'tiring', 'infectious', 'shit', 'gold', 'ill-advised', 'goddamned', 'angst-filled', 'foul', 'elegant', 'gargantuan', 'hot', 'predictable', 'amusing', 'best', 'gritty', 'unique', 'memorable', 'respectable', 'happy', 'understandable', 'nicest', 'brilliant', 'positive', 'angry', 'awesome', 'ridiculous', 'sad', 'prime', 'worried', 'unlikeable', 'favorite', 'unreliable', 'forgettable', 'corniest', 'sucked', 'unsettling', 'cryptic', 'reliable', 'funny', 'curious', 'appropriate', 'considerable', 'incomplete', 'concerned', 'excessive', 'anxious', 'great', 'perfect', 'legendary', 'pompous', 'delightful', 'enigmatic', 'monumental', 'empathetic', 'hilarious', 'scary', 'scare', 'staggered', 'crappy', 'painful', 'awed', 'misogynistic', 'hypocrite', 'trivial', 'catastrophic', 'pretentious', 'unspeakable', 'magnetic', 'controversial', 'appreciate', 'shameful', 'flawless', 'unremorseful', 'grave', 'preferred', 'nasty', 'horrendous', 'petty', 'selfless', 'phenomenal', 'adorable', 'emotional', 'interested', 'unwilling', 'grateful', 'distasteful', 'enjoyable', 'unlovable', 'unimpressive', 'intrigued', 'attached', 'explosive', 'valuable', 'spectacular', 'superfluous', 'unputdownable', 'dreadful', 'inspired', 'underwhelming', 'terrible', 'sensual', 'superior', 'lit', 'pretty', 'horrid', 'uncanny', 'disruptive', 'marvelous', 'nonsense', 'amateurish', 'dull', 'virtuous', 'wonderful', 'fearsome', 'wondrous', 'keen', 'powerful', 'cartoonish', 'unadulterated', 'awe', 'prickly', 'horrible', 'fantastic', 'unforgettable', 'yucky', 'annoyed', 'bad', 'unenlightened', 'unpleasant', 'captivated', 'enjoyable', 'exotic', 'cheesy', 'gripped', 'grim', 'notable', 'despicable', 'romantic', 'deep', 'gaslight', 'vile', 'hideous', 'favourable', 'disastrous', 'unbearable', 'sharp', 'lousy', 'exquisite', 'pathetic', 'pleasant', 'extraordinary', 'laughable', 'insightful', 'insufferable', 'significant', 'unenjoyable', 'cynical', 'fun', 'foolish', 'humorous', 'underdeveloped', 'epic', 'agreeable', 'lame', 'finest', 'comfortable', 'absurd', 'remorseful', 'exceptional', 'glorious', 'tremendous', 'frustrating', 'likable', 'marketable', 'excellent', 'hypnotic', 'marvellous', 'lovable', 'euphoric', 'questionable', 'heinous', 'remarkable', 'impressive', 'unbelievable', 'hurtful', 'ideal', 'untrustworthy', 'good', 'awful', 'outstanding', 'cleverly', 'distinctive', 'likeable', 'unendurable', 'intense', 'impressed', 'smitten', 'understatement', 'impatient', 'unforgivable', 'untouchable', 'shallow', 'asshole', 'typical', 'utter', 'inventive', 'masterful', 'decent', 'wild', 'attractive', 'rare', 'unlikable', 'sick', 'frustrate']

# preprocess text data

text = re.sub(r'[^\x00-\x7F]+','', text)

text = text.lower().replace(".", "").replace("-"," ").replace("_"," ").replace('"',"").replace("'","")

text = re.sub(r'\d+', '', text)

text = text.lower()

text = re.split('\.|\?|\!|\,|\(|\)|\:|\`|\;',text)

# negation_words = do_stem(negation_words)

# corpus = do_stem(corpus)

token = []

for sent in text:

    token += tokenize(sent)

rank = {}
for t in token:
    if t in rank:
        rank[t] += 1
    else:
        rank[t] = 0

count = 0

obj = []
for key, value in sorted(rank.iteritems(), key=lambda (k,v): (v,k), reverse = True):
    obj.append(key)

token = nltk.pos_tag(obj)
obj = []
for t in token:
    if count == 142:
        break
    if t[0] not in corpus:
        if t[1] in ["JJ","JJS","JJC","VB","VBP","RB","NN"]:
            if len(t[0]) > 1: 
                if t[0] not in negation_words:
                    obj.append(t[0])
                    count += 1
print obj