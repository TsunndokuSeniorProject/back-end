from gensim.models import Word2Vec
from gensim.test.utils import common_texts
from gensim.utils import simple_preprocess, deaccent, tokenize, simple_tokenize
from nltk.corpus import stopwords
import nltk
import sys
sys.path.append("../")
from file_reader import file_reader
from oms import opinion_mining_system
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

train_set = []
train_direc = "C:/Users/USER/Downloads/neo_sentences_filtered.txt"

stop_words = set(stopwords.words('english'))

with open(train_direc, 'r', encoding='utf-8') as f:
    data = f.readlines()
f.close()

threshold = 0.50


# embeddings_index = {}
# f = open('C:/Users/USER/Back-end/model/vectors/glove.6B.100d.txt', encoding='utf-8')
# for line in f:
#     values = line.split()
#     word = values[0]
#     coefs = np.asarray(values[1:], dtype='float32')
#     embeddings_index[word] = coefs
# f.close()
print(stop_words)
processed = []
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

model = Word2Vec(processed)

print("start training")
model.train(processed, total_examples=len(processed), epochs=10)
print("training finished")

# model.save("gensim_model.sav")
# model = Word2Vec.load('gensim_model.sav')

# uncomment to write to file
writeout = ""
for word, vector in zip(model.wv.index2word, model.wv.vectors):
    writeout = writeout + word + " " + str(list(vector)) + "\n"

with open('gensim_vec.txt', 'w+', encoding='utf8') as fp:
    fp.write(writeout)
fp.close()


test_set = []
test_direc = "C:/Users/USER/Downloads/test.txt"

test_set, test_label = file_reader().read(test_direc)

aspects = opinion_mining_system().operate_aspect_extraction(test_set)

print(aspects)
# print(test_label)
while threshold <= 0.9:
    res = []
    print("test_set length: {}".format(len(test_set)))
    print("aspect lenght: {}".format(len(aspects)))
    for sen, aspect in zip(test_set, aspects):
        asp_in_sen = []
        for ele in aspect:
            if ele.lower() in sen.lower():
                a = dict()
                try:
                    a['story_sim'] = model.similarity('story', ele.lower())
                    a['char_sim'] = model.similarity('impchar', ele.lower())
                    if model.similarity('character', ele.lower()) > a['char_sim']:
                        a['char_sim'] = model.similarity('character', ele.lower())
                    a['writing_sim'] = model.similarity('writing', ele.lower())
                    # if model.similarity('novel', ele.lower()) > a['writing_sim']:
                    #     a['writing_sim'] = model.similarity('novel', ele.lower())
                    max_sim = max(a.values())
                    
                    if max_sim < threshold:
                        a = 0
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
                    a = 0
                    # asp_in_sen.append(-99)
        res.append(asp_in_sen)
    
# while threshold <= 1:
#     res = []
#     for sen in test_set:
#         for aspect in aspects:
#             if ele.lower() in sen.lower():
#                 a = dict()
#                 try:
#                     a['story_sim'] = cosine_similarity([embeddings_index['story']], [embeddings_index[ele.lower()]])
#                     a['char_sim'] = cosine_similarity([embeddings_index['character']], [embeddings_index[ele.lower()]])
#                     a['writing_sim'] = cosine_similarity([embeddings_index['writing']], [embeddings_index[ele.lower()]])
#                     max_sim = max(a.values())
#                     if max_sim < threshold:
#                         res.append(-99)
#                     else:
#                         for asp, sim in a.items():
#                             if max_sim == sim:
#                                 if asp == 'story_sim':
#                                     res.append(1)
#                                 elif asp == 'writing_sim':
#                                     res.append(2)
#                                 elif asp == 'char_sim':
#                                     res.append(3)
#                 except KeyError:
#                     res.append(-99)


    correct, total = 0, 0

    for sen, pred, label in zip(test_set, res, test_label):
        if not pred:
            continue
        else:
            # print("Sentence : {} predict : {} , actual : {}".format(sen, pred[0], label))
            if pred[0] == -99:
                continue
            else:
                if pred[0] == label:
                    correct += 1
                total += 1

    print("Threshold: " + str(threshold))
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
                    if pred[0] == label:
                        correct += 1
                    total += 1

    print("Threshold: " + str(threshold))
    print("Acc: " + str(correct/total))
    print("Correct: " + str(correct))
    print("Total: " + str(total))
    threshold += 0.05