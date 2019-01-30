# tf idf
# position
# POS
# seed word {pos_adj} {neg_adj}
# negation : not infront of [adv]? adj
# modifier : [adv]? adj
import random
import numpy as np
import os
import json
import re
import string
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from autocorrect import spell
from nltk import word_tokenize
from nltk.stem.porter import PorterStemmer


def tokenize(text):
    tokens = word_tokenize(text)
    return tokens

def create_word_feature(corpus,all_reviews_sentence):
    all_reviews_sentence = re.sub(r'[^\x00-\x7F]+',' ', all_reviews_sentence)

    all_reviews_sentence = all_reviews_sentence.lower().replace(".", " ").replace("-"," ").replace("_"," ").replace("/", " ")
    all_reviews_sentence = re.sub(r'\d+', '', all_reviews_sentence)

    all_reviews_sentence = re.split('\.|\?|\!',all_reviews_sentence)

    all_reviews_sentence = [" ".join(tokenize(txt.lower())) for txt in all_reviews_sentence]

    vectorizer = TfidfVectorizer()
    matrix = vectorizer.fit_transform(all_reviews_sentence).todense()
    matrix = pd.DataFrame(matrix, columns=vectorizer.get_feature_names())
    top_words = matrix.sum(axis=0).sort_values(ascending=False)
    token = list(matrix.keys())

    index = 0
    word_feature = []
    word_map = []
    for sentence in all_reviews_sentence:
        for word in token:
            if word in sentence:
                if word in corpus:
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

                    word_feature.append([matrix[word].loc[index], position, POS, nega])
                    word_map.append(word)
        index += 1
    return word_feature, word_map


def create_word_feature_test_set(all_reviews_sentence):
    all_reviews_sentence = re.sub(r'[^\x00-\x7F]+','', all_reviews_sentence)

    all_reviews_sentence = all_reviews_sentence.lower().replace(".", "").replace("-"," ").replace("_"," ").replace("/","")
    all_reviews_sentence = re.sub(r'\d+', '', all_reviews_sentence)

    all_reviews_sentence = re.split('\.|\?|\!',all_reviews_sentence)

    all_reviews_sentence = [" ".join(tokenize(txt.lower())) for txt in all_reviews_sentence]

    vectorizer = TfidfVectorizer()
    matrix = vectorizer.fit_transform(all_reviews_sentence).todense()
    matrix = pd.DataFrame(matrix, columns=vectorizer.get_feature_names())
    top_words = matrix.sum(axis=0).sort_values(ascending=False)
    token = list(matrix.keys())

    index = 0
    word_feature = []
    word_map = []
    for sentence in all_reviews_sentence:
        for word in token:
            if word in sentence:
                # if word in corpus:
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

                word_feature.append([matrix[word].loc[index], position, POS, nega])
                word_map.append(word)
        index += 1
    return word_feature, word_map


if __name__ == "__main__":
    directory = "../web_scraper/goodreads/novel/crime/"
    books = [name for name in os.listdir(directory)]

    all_reviews_text = ""

    for book in books:
        if book != ".DS_Store":
            with open(directory+book, 'r') as fp:
                data = json.load(fp)
                fp.close()
            for review in data['Reviews']:
                all_reviews_text = all_reviews_text + review['Review'] + " "

    negation_words = ["imperfect","impossible","inelegant","insane","misunderstood","unfair","unfavorable","unhappy","unhealthy","unjust","unlucky","unpleasant","unsatisfactory","unsightly","untoward","unwanted","unwelcome","unwholesome","unwieldy","unwise","worthless","never","neigther","nobody","no","none","nor","nothing","nowhere","not","n't"]
    subjectivity_corpus = ['foul', 'elegant', 'gargantuan', 'hot', 'predictable', 'amusing', 'best', 'gritty', 'unique', 'memorable', 'respectable', 'happy', 'understandable', 'nicest', 'brilliant', 'positive', 'angry', 'awesome', 'ridiculous', 'sad', 'prime', 'worried', 'unlikeable', 'favorite', 'unreliable', 'forgettable', 'corniest', 'sucked', 'unsettling', 'cryptic', 'reliable', 'funny', 'curious', 'appropriate', 'considerable', 'incomplete', 'concerned', 'excessive', 'anxious', 'great', 'perfect', 'legendary', 'pompous', 'delightful', 'enigmatic', 'monumental', 'empathetic', 'hilarious', 'scary', 'scare', 'staggered', 'crappy', 'painful', 'awed', 'misogynistic', 'hypocrite', 'trivial', 'catastrophic', 'pretentious', 'unspeakable', 'magnetic', 'controversial', 'appreciate', 'shameful', 'flawless', 'unremorseful', 'grave', 'preferred', 'nasty', 'horrendous', 'petty', 'selfless', 'phenomenal', 'adorable', 'emotional', 'interested', 'unwilling', 'grateful', 'distasteful', 'enjoyable', 'unlovable', 'unimpressive', 'intrigued', 'attached', 'explosive', 'valuable', 'spectacular', 'superfluous', 'unputdownable', 'dreadful', 'inspired', 'underwhelming', 'terrible', 'sensual', 'superior', 'lit', 'pretty', 'horrid', 'uncanny', 'disruptive', 'marvelous', 'nonsense', 'amateurish', 'dull', 'virtuous', 'wonderful', 'fearsome', 'wondrous', 'keen', 'powerful', 'cartoonish', 'unadulterated', 'awe', 'prickly', 'horrible', 'fantastic', 'unforgettable', 'yucky', 'annoyed', 'bad', 'unenlightened', 'unpleasant', 'captivated', 'enjoyable', 'exotic', 'cheesy', 'gripped', 'grim', 'notable', 'despicable', 'romantic', 'deep', 'gaslight', 'vile', 'hideous', 'favourable', 'disastrous', 'unbearable', 'sharp', 'lousy', 'exquisite', 'pathetic', 'pleasant', 'extraordinary', 'laughable', 'insightful', 'insufferable', 'significant', 'unenjoyable', 'cynical', 'fun', 'foolish', 'humorous', 'underdeveloped', 'epic', 'agreeable', 'lame', 'finest', 'comfortable', 'absurd', 'remorseful', 'exceptional', 'glorious', 'tremendous', 'frustrating', 'likable', 'marketable', 'excellent', 'hypnotic', 'marvellous', 'lovable', 'euphoric', 'questionable', 'heinous', 'remarkable', 'impressive', 'unbelievable', 'hurtful', 'ideal', 'untrustworthy', 'good', 'awful', 'outstanding', 'cleverly', 'distinctive', 'likeable', 'unendurable', 'intense', 'impressed', 'smitten', 'understatement', 'impatient', 'unforgivable', 'untouchable', 'shallow', 'asshole', 'typical', 'utter', 'inventive', 'masterful', 'decent', 'wild', 'attractive', 'rare', 'unlikable', 'sick', 'frustrate']
    objectivity_corpus = [u'book', u'read', u'have', u'so', u'be', u'story', u'are', u'about', u'first', u'just', u'there', u'series', u'very', u'well', u'really', u'im', u'novel', u'reading', u'love', u'time', u'much', u'mystery', u'get', u'author', u'new', u'then', u'character', u'even', u'only', u'way', u'am', u'plot', u'other', u'murder', u'too', u'many', u'little', u'also', u'didnt', u'review', u'ive', u'now', u'do', u'detective', u'thriller', u'still', u'say', u'crime', u'jack', u'back', u'feel',u'long', u'life', u'think', u'here', u'bit', u'find', u'wasnt', u'go', u'see', u'right', u'killer', u'something', u'enjoyed', u'end', u'day', u'last', u'dark', u'lot', u'work', u'old', u'case', u'woman', u'interesting', u'man', u'make', u'such', u'few', u'again', u'year', u'second', u'page', u'ever', u'cant', u'want', u'part', u'felt', u'always', u'train', u'thing', u'start', u'once', u'novels', u'main', u'full', u'friend', u'actually', u'enough', u'home', u'sure', u'same', u'world', u'reacher', u'own', u'keep', u'true', u'family', u'doesnt', u'different', u'take', u'quite', u'mind', u'blood', u'together', u'th', u'serial', u'kind', u'hard', u'give', u'whole', u'lisbeth', u'couple', u'strike', u'fiction', u'couldnt', u'husband', u'fan', u'fact', u'psychological', u'yet', u'kept', u'style', u'que', u'high', u'definitely', u'debut', u'agatha', u'fast', u'everything', u'copy', u'bosch', u'ballard', u'young', u'real', u'isnt', u'however', u'action', u'id', u'gillian', u'come', u'already', u'suspense', u'someone', u'later', u'cold', u'christie', u'taylor', u'night', u'maybe', u'half', u'everyone', u'big', u'annabelle', u'almost', u'wait', u'several', u'lost', u'flynn', u'far', u'write', u'reader', u'fbi', u'especially', u'death', u'ben', u'baby', u'ago', u'yes', u'son', u'sherlock', u'point', u'london', u'line', u'late', u'la', u'anything', u'able', u'youre', u'town', u'team', u'previous', u'place', u'netgalley', u'movie', u'house', u'emma', u'sophie', u'side', u'show', u'idea', u'body', u'absolutely', u'soon', u'slow', u'salander', u'rather', u'let']
    subj_corrected = []
    obj_corrected = []
    
    for subj in subjectivity_corpus:
        subj_corrected.append(spell(subj))
    for obj in objectivity_corpus:
        obj_corrected.append(spell(obj))

    sub_word_feature, sub_word = create_word_feature(subjectivity_corpus, all_reviews_text)
    print(sub_word)
    ob_word_feature, ob_word = create_word_feature(objectivity_corpus, all_reviews_text)

    print(len(sub_word_feature))

    ob_word_feature = random.sample(ob_word_feature, 5411)
    print(len(ob_word_feature))
    sub_ans = [1 for x in sub_word_feature]
    ob_ans = [0 for x in ob_word_feature]
    train = sub_word_feature+ob_word_feature
    answer_label = sub_ans+ob_ans
    with open("./train.json", 'w+') as fp:
        json.dump({
            "train":train,
            "class":answer_label
        },fp)
        fp.close()
    directory = "../web_scraper/goodreads/novel/crime/"
    books = [name for name in os.listdir(directory)]


    all_reviews_text = ""

    for book in books:
        if book != ".DS_Store":
            with open(directory+book, 'r') as fp:
                data = json.load(fp)
                fp.close()
            for review in data['Reviews']:
                all_reviews_text = all_reviews_text + review['Review'] + " "

    word_feature, word_map = create_word_feature_test_set(all_reviews_text)

    with open("./test_set.json", 'w+') as fp:
        json.dump({
            "test":word_feature,
            "word":word_map
        },fp)
        fp.close()
