
import random
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
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from autocorrect import spell


class word_feature:
    def __init__(self):
        self.negation_words = ["imperfect","impossible","inelegant","insane","misunderstood","unfair","unfavorable","unhappy","unhealthy","unjust","unlucky","unpleasant","unsatisfactory","unsightly","untoward","unwanted","unwelcome","unwholesome","unwieldy","unwise","worthless","never","neigther","nobody","no","none","nor","nothing","nowhere","not","n't"]
    def tokenize(self, text):
        tokens = word_tokenize(text)
        return tokens

    def create_word_feature(self, corpus,all_reviews_sentence):

        new_corpus = [spell(cp) for cp in corpus]

        all_reviews_sentence = re.sub(r'[^\x00-\x7F]+','', all_reviews_sentence)
        all_reviews_sentence = all_reviews_sentence.lower().replace(".", "").replace("-"," ").replace("_"," ").replace("/","")
        all_reviews_sentence = re.sub(r'\d+', '', all_reviews_sentence)
        all_reviews_sentence = re.split('\.|\?|\!',all_reviews_sentence)
        all_reviews_sentence = [" ".join(self.tokenize(txt.lower())) for txt in all_reviews_sentence]
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
                    if word in new_corpus:
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
                        if word in self.negation_words:
                            nega = 1

                        word_feature.append([matrix[word].loc[index], position, POS, nega])
                        word_map.append(word)
            index += 1
        return word_feature, word_map, all_reviews_sentence

    def create_word_feature_test_set(self, all_reviews_sentence):
        all_reviews_sentence = re.sub(r'[^\x00-\x7F]+','', all_reviews_sentence)
        all_reviews_sentence = all_reviews_sentence.lower().replace(".", "").replace("-"," ").replace("_"," ").replace("/","")
        all_reviews_sentence = re.sub(r'\d+', '', all_reviews_sentence)
        all_reviews_sentence = re.split('\.|\?|\!',all_reviews_sentence)
        all_reviews_sentence = [" ".join(self.tokenize(txt.lower())) for txt in all_reviews_sentence]
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
                    if word in self.negation_words:
                        nega = 1

                    word_feature.append([matrix[word].loc[index], position, POS, nega])
                    word_map.append(word)
            index += 1
        return word_feature, word_map, all_reviews_sentence

    def test(self):
        print ("okay plss wait")


class sentence_selector:
    def filter(self, sentences_list, subjectivity_word_list):
        filtered_sentence = []
        for sentence in sentences_list:
            for word in subjectivity_word_list:
                if word in sentence:
                    filtered_sentence.append(sentence)
                    break
        return filtered_sentence
if __name__ == "__main__":

    wf = word_feature()
    wf.test()
    # directory = "../web_scraper/goodreads/novel/crime/"
    # books = [name for name in os.listdir(directory)]
    # all_reviews_text = ""
    # for book in books:
    #     if book != ".DS_Store":
    #         with open(directory+book, 'r') as fp:
    #             data = json.load(fp)
    #             fp.close()
    #         for review in data['Reviews']:
    #             all_reviews_text = all_reviews_text + review['Review'] + " "
        
    
    subjectivity_corpus = ['foul', 'elegant', 'gargantuan', 'hot', 'predictable', 'amusing', 'best', 'gritty', 'unique', 'memorable', 'respectable', 'happy', 'understandable', 'nicest', 'brilliant', 'positive', 'angry', 'awesome', 'ridiculous', 'sad', 'prime', 'worried', 'unlikeable', 'favorite', 'unreliable', 'forgettable', 'corniest', 'sucked', 'unsettling', 'cryptic', 'reliable', 'funny', 'curious', 'appropriate', 'considerable', 'incomplete', 'concerned', 'excessive', 'anxious', 'great', 'perfect', 'legendary', 'pompous', 'delightful', 'enigmatic', 'monumental', 'empathetic', 'hilarious', 'scary', 'scare', 'staggered', 'crappy', 'painful', 'awed', 'misogynistic', 'hypocrite', 'trivial', 'catastrophic', 'pretentious', 'unspeakable', 'magnetic', 'controversial', 'appreciate', 'shameful', 'flawless', 'unremorseful', 'grave', 'preferred', 'nasty', 'horrendous', 'petty', 'selfless', 'phenomenal', 'adorable', 'emotional', 'interested', 'unwilling', 'grateful', 'distasteful', 'enjoyable', 'unlovable', 'unimpressive', 'intrigued', 'attached', 'explosive', 'valuable', 'spectacular', 'superfluous', 'unputdownable', 'dreadful', 'inspired', 'underwhelming', 'terrible', 'sensual', 'superior', 'lit', 'pretty', 'horrid', 'uncanny', 'disruptive', 'marvelous', 'nonsense', 'amateurish', 'dull', 'virtuous', 'wonderful', 'fearsome', 'wondrous', 'keen', 'powerful', 'cartoonish', 'unadulterated', 'awe', 'prickly', 'horrible', 'fantastic', 'unforgettable', 'yucky', 'annoyed', 'bad', 'unenlightened', 'unpleasant', 'captivated', 'enjoyable', 'exotic', 'cheesy', 'gripped', 'grim', 'notable', 'despicable', 'romantic', 'deep', 'gaslight', 'vile', 'hideous', 'favourable', 'disastrous', 'unbearable', 'sharp', 'lousy', 'exquisite', 'pathetic', 'pleasant', 'extraordinary', 'laughable', 'insightful', 'insufferable', 'significant', 'unenjoyable', 'cynical', 'fun', 'foolish', 'humorous', 'underdeveloped', 'epic', 'agreeable', 'lame', 'finest', 'comfortable', 'absurd', 'remorseful', 'exceptional', 'glorious', 'tremendous', 'frustrating', 'likable', 'marketable', 'excellent', 'hypnotic', 'marvellous', 'lovable', 'euphoric', 'questionable', 'heinous', 'remarkable', 'impressive', 'unbelievable', 'hurtful', 'ideal', 'untrustworthy', 'good', 'awful', 'outstanding', 'cleverly', 'distinctive', 'likeable', 'unendurable', 'intense', 'impressed', 'smitten', 'understatement', 'impatient', 'unforgivable', 'untouchable', 'shallow', 'asshole', 'typical', 'utter', 'inventive', 'masterful', 'decent', 'wild', 'attractive', 'rare', 'unlikable', 'sick', 'frustrate']
    objectivity_corpus = ['book', 'wa', 'read', 'have', 'be', 'so', 'charact', 'are', 'ha', 'first', 'just', 'novel', 'time', 'veri', 'get', 'mysteri', 'well', 'realli', 'author', 'im', 'go', 'murder', 'write', 'know', 'review', 'much', 'start', 'end', 'work', 'thing', 'new', 'plot', 'feel', 'year', 'then', 'make', 'way', 'other', 'becaus', 'even', 'onli', 'do', 'star', 'say', 'am', 'want', 'think', 'find', 'too', 'mani', 'littl', 'crime', 'also', 'happen', 'dont', 'detect', 'page', 'didnt', 'ive', 'take', 'see', 'now', 'day', 'come', 'everi', 'down', 'still', 'lot', 'peopl', 'seem', 'jack', 'bit', 'back', 'set', 'here', 'long', 'life', 'give', 'friend', 'turn', 'right','wasnt', 'someth', 'case', 'twist', 'part', 'last', 'dark', 'befor', 'investig', 'woman', 'look', 'old', 'keep', 'begin', 'next', 'tri', 'man', 'whi', 'polic', 'person', 'actual', 'such', 'reader', 'second', 'few', 'doe', 'call', 'main', 'again', 'fiction', 'wait', 'ever', 'cant', 'finish', 'train', 'use', 'place', 'alway', 'onc', 'mind', 'live', 'differ', 'famili', 'full', 'fan', 'sure', 'miss', 'home', 'strike', 'own', 'husband', 'holm', 'enough', 'world', 'publish', 'kind', 'show', 'same', 'quit', 'name', 'final', 'coupl', 'christi', 'lisbeth', 'follow', 'detail', 'true', 'thank', 'serial', 'hope', 'doesnt', 'blood', 'around', 'hard', 'fact', 'th','excit', 'chapter', 'whole', 'surpris', 'psycholog', 'pick', 'need', 'learn', 'kill', 'tell', 'movi', 'expect', 'definit', 'couldnt', 'copi', 'style', 'move', 'becom', 'word', 'reason', 'decid', 'action', 'yet', 'que', 'meet', 'line', 'let', 'heart', 'guess', 'writer', 'watch', 'point', 'high', 'debut', 'ballard', 'agatha', 'absolut', 'team', 'night', 'mean', 'late', 'howev', 'fast', 'everyth', 'cover', 'bosch', 'young', 'sever', 'real', 'pace']
    # sub_word_feature, sub_word, all_sub_reviews_sentence = wf.create_word_feature(subjectivity_corpus, all_reviews_text)
    # ob_word_feature, ob_word, all_ob_reviews_sentence = wf.create_word_feature(objectivity_corpus, all_reviews_text)
    # ob_word_feature = random.sample(ob_word_feature, 2458)
    # sub_word_feature = random.sample(sub_word_feature, 2458)
    # sub_ans = [1 for x in sub_word_feature]
    # ob_ans = [0 for x in ob_word_feature]
    # train = sub_word_feature+ob_word_feature
    # answer_label = sub_ans+ob_ans
    # with open("./train.json", 'w+') as fp:
    #     json.dump({
    #         "train":train,
    #         "class":answer_label
    #     },fp)
    #     fp.close()
    # directory = "../web_scraper/goodreads/novel/crime/"
    # books = [name for name in os.listdir(directory)]

    # all_reviews_text = ""

    # for book in books:
    #     if book != ".DS_Store":
    #         with open(directory+book, 'r') as fp:
    #             data = json.load(fp)
    #             fp.close()
    #         for review in data['Reviews']:
    #             all_reviews_text = all_reviews_text + review['Review'] + " "
        
    # word_feature, word_map, all_reviews_sentence = wf.create_word_feature_test_set(all_reviews_text)

    # with open("./test_set.json", 'w+') as fp:
    #     json.dump({
    #         "test":word_feature,
    #         "word":word_map
    #     },fp)
    #     fp.close()
    word_feature, word_map, all_reviews_sentence = wf.create_word_feature_test_set("this shiT is noob as fuck")
    print word_feature, word_map