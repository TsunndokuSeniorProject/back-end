from gensim.models import Word2Vec, KeyedVectors
from gensim.test.utils import common_texts
from gensim.utils import simple_preprocess, deaccent, tokenize, simple_tokenize
from nltk.corpus import stopwords
import nltk
import sys
sys.path.append("../")
from model.file_reader import file_reader
from model.oms import opinion_mining_system
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import model.text_processor

class gensim_w2v:
    def __init__(self):
        self.threshold = 0.5
        self.EMBEDDING_DIM = 100
        self.model = Word2Vec()
        
        self.story_core = ['story', 'plot', 'bookname', 'intrigue']
        self.char_core = ['character', 'protagonist', 'impchar', 'cast', 'villain']
        self.writing_core = ['written', 'dialogue', 'authname', 'writing', 'pacing']


    def train(self, input_text=None):
        train_set = []
        train_direc = "C:/Users/hpEnvy/Desktop/raw_review_latest.txt"
        with open(train_direc, 'r', encoding='utf-8') as f:
            data = f.readlines()
        f.close()

        stop_words = set(stopwords.words('english'))
        processed = []
        print("start simple_preprocess")
        for sentence in data:
            if len(sentence) > 2:
                temp = simple_preprocess(sentence)
                ready_to_add = []
                for each in temp:
                    if each not in stop_words:
                        ready_to_add.append(each)
                processed.append(ready_to_add)
            # if len(sentence) > 2:
            #     processed.append(simple_preprocess(sentence))
        print("end simple_preprocess")
        self.model = Word2Vec(processed)

        print("start training")
        self.model.train(processed, total_examples=len(processed), epochs=10)
        print("training finished")
        
        self.model.wv.save('./model/wordvectors.kv')

    # # uncomment to write to file
    # writeout = ""
    # for word, vector in zip(model.wv.index2word, model.wv.vectors):
    #     writeout = writeout + word + " " + str(list(vector)) + "\n"

    # with open('gensim_vec.txt', 'w+', encoding='utf8') as fp:
    #     fp.write(writeout)
    # fp.close()

    def test(self, input_text=None):
        wv = KeyedVectors.load('./model/wordvectors.kv', mmap='r')
        test_set = []
        test_direc = "C:/Users/hpEnvy/Downloads/test.txt"
        test_set, test_label = file_reader().read(test_direc)

        aspects = opinion_mining_system().operate_aspect_extraction(test_set)
        print(aspects)
        while self.threshold <= 0.9:
            res = []
            print("test_set length: {}".format(len(test_set)))
            print("aspect lenght: {}".format(len(aspects)))
            for sen, aspect in zip(test_set, aspects):
                asp_in_sen = []
                for ele in aspect:
                    if ele.lower() in sen.lower():
                        a = dict()
                        a['story_sim'] = 0
                        a['char_sim'] = 0
                        a['writing_sim'] = 0
                        try:
                            
                            for core in self.story_core:
                                try :
                                    if wv.similarity(core.lower(), ele.lower()) > a['story_sim']:
                                        a['story_sim'] = wv.similarity(core.lower(), ele.lower())
                                except KeyError:
                                    pass
                            
                            for core in self.writing_core:
                                try :
                                    if wv.similarity(core.lower(), ele.lower()) > a['writing_sim']:
                                        a['writing_sim'] = wv.similarity(core.lower(), ele.lower())
                                except KeyError:
                                    pass
                            
                            for core in self.char_core:
                                try :
                                    if wv.similarity(core.lower(), ele.lower()) > a['char_sim']:
                                        a['char_sim'] = wv.similarity(core.lower(), ele.lower())
                                except KeyError:
                                    pass
                                                               
                            max_sim = max(a.values())
                            
                            
                        except KeyError:
                            pass
                            # asp_in_sen.append(-99)
                        if max_sim < self.threshold:
                            pass
                            # asp_in_sen.append(-99)
                        else:
                            # print(ele.lower())
                            for asp, sim in a.items():
                                if max_sim == sim:
                                    if asp == 'story_sim':
                                        asp_in_sen.append(1)
                                    elif asp == 'writing_sim':
                                        asp_in_sen.append(2)
                                    elif asp == 'char_sim':
                                        asp_in_sen.append(3)
                res.append(asp_in_sen)

            correct, total = 0, 0
            
            for sen, pred, label in zip(test_set, res, test_label):
                if not pred:
                    continue
                else:
                    # print("Sentence : {} predict : {} , actual : {}".format(sen, pred[0], label))               
                    if label in pred:
                        correct += 1
                    total += 1

            print("Threshold: " + str(self.threshold))
            print("Acc: " + str(correct/total))
            print("Correct: " + str(correct))
            print("Total: " + str(total))

            correct, total = 0, 0

            for sen, pred, label in zip(test_set, res, test_label):
                if label != 2:
                    if not pred:
                        continue
                    else:
                        # print("Sentence : {} predict : {} , actual : {}".format(sen, pred[0], label))
                        if pred[0] == -99:
                            continue
                        else:
                            if label in pred:
                                correct += 1
                            total += 1

            print("Threshold: " + str(self.threshold))
            print("Acc: " + str(correct/total))
            print("Correct: " + str(correct))
            print("Total: " + str(total))
            self.threshold += 0.05


    def predict(self, input_text):
        wv = KeyedVectors.load('./model/wordvectors.kv', mmap='r')
        pred_res = []
        print("start oms")
        aspects = opinion_mining_system().operate_aspect_extraction(input_text)
        
        print("end oms")
        
        for sen, aspect in zip(input_text, aspects):
            asp_in_sen = []
            for ele in aspect:
                if ele.lower() in sen.lower():
                    a = dict()
                    a['story_sim'] = 0
                    a['char_sim'] = 0
                    a['writing_sim'] = 0
                    try:
                        for core in self.story_core:
                            try :
                                if wv.similarity(core.lower(), ele.lower()) > a['story_sim']:
                                    a['story_sim'] = wv.similarity(core.lower(), ele.lower())
                            except KeyError:
                                pass
                        
                        for core in self.writing_core:
                            try :
                                if wv.similarity(core.lower(), ele.lower()) > a['writing_sim']:
                                    a['writing_sim'] = wv.similarity(core.lower(), ele.lower())
                            except KeyError:
                                pass
                        
                        for core in self.char_core:
                            try :
                                if wv.similarity(core.lower(), ele.lower()) > a['char_sim']:
                                    a['char_sim'] = wv.similarity(core.lower(), ele.lower())
                            except KeyError:
                                pass

                        try:
                            max_sim = max(a.values())
                        except ValueError:
                            max_sim = 0
                            pass
                        if max_sim < 0.7:
                            continue
                            # asp_in_sen.append(-99)
                        else:
                            # print(ele.lower())
                            for asp, sim in a.items():
                                if max_sim == sim:
                                    if asp == 'story_sim':
                                        asp_in_sen.append(1)
                                    elif asp == 'writing_sim':
                                        asp_in_sen.append(2)
                                    elif asp == 'char_sim':
                                        asp_in_sen.append(3)
                    except KeyError:
                        continue
                        # asp_in_sen.append(-99)
            pred_res.append(asp_in_sen)
        
        return pred_res


    # def writeout(self, towrite):

    
if __name__ == '__main__':
    w2v = gensim_w2v()
    
    # superraw_direc = "C:/Users/hpEnvy/Desktop/raw_review_v1.txt"
    
    w2v.train()
    w2v.test()
    # print(w2v.predict(["hello, mama", 'The book has the best character and dialogue ive ever seen', 'impchar was great']))
    
    direc = 'C:/Users/hpEnvy/Desktop/raw_review_latest.txt'
    with open(direc, 'r', encoding='utf8') as fp:
        pre_data = fp.readlines()
    fp.close()
    
    
    result = w2v.predict(pre_data)
    
    towrite = ""
    # with open(superraw_direc, 'r', encoding='utf8') as fp:
    #     con_data = fp.readlines()
    # fp.close()

    # for sen, pred in zip(pre_data, result):
    #     if not pred:
    #         continue
    #     else:
    #         towrite += sen + " ," + str(pred) + "\n"

    
    # with open('C:/Users/hpEnvy/Desktop/labeled_by_gensim_for_bayes.txt', 'w+', encoding='utf8') as fp:
    #     fp.write(towrite)