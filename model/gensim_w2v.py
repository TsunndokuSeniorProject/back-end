from gensim.models import Word2Vec
from gensim.test.utils import common_texts
from gensim.utils import simple_preprocess, deaccent, tokenize, simple_tokenize
import sys
sys.path.append("../")
from file_reader import file_reader
from oms import opinion_mining_system
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from text_processor import tag_character

train_set = []
train_direc = "C:/Users/USER/Downloads/neo_sentences_filtered.txt"

with open(train_direc, 'r', encoding='utf-8') as f:
    data = f.readlines()
f.close()

threshold = 0.70


# embeddings_index = {}
# f = open('C:/Users/USER/Back-end/model/vectors/glove.6B.100d.txt', encoding='utf-8')
# for line in f:
#     values = line.split()
#     word = values[0]
#     coefs = np.asarray(values[1:], dtype='float32')
#     embeddings_index[word] = coefs
# f.close()

processed = []
for sentence in data:
    if len(sentence) > 1:
        processed.append(simple_preprocess(sentence))

model = Word2Vec(processed)

print("start training")
model.train(processed, total_examples=len(processed), epochs=10)
print("training finished")

print(model.wv.most_similar(positive='story'))
print(model.wv.most_similar(positive='character'))
print(model.wv.most_similar(positive='writing'))
print(model.wv.most_similar(positive='imp_char'))
test_set = []
test_direc = "C:/Users/USER/Downloads/test.txt"

test_set, test_label = file_reader().read(test_direc)

aspects = opinion_mining_system().operate_aspect_extraction(test_set)

print(aspects)
# print(test_label)
# while threshold <= 0.9:
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
                a['char_sim'] = model.similarity('imp_char', ele.lower())
                if model.similarity('character', ele.lower()) > a['char_sim']:
                    a['char_sim'] = model.similarity('character', ele.lower())
                a['writing_sim'] = model.similarity('writing', ele.lower())
                max_sim = max(a.values())
                
                if max_sim < threshold:
                    asp_in_sen.append(-99)
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
                asp_in_sen.append(-99)
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
    print("Sentence : {} predict : {} , actual : {}".format(sen, pred, label))
    if pred is None:
        continue
    if pred == -99:
        continue
    else:
        if pred == label:
            correct += 1
        total += 1

print("Threshold: " + str(threshold))
print("Acc: " + str(correct/total))
print("Correct: " + str(correct))
print("Total: " + str(total))

correct, total = 0, 0

for sen, pred, label in zip(test_set, res, test_label):
    if label != 2:
        if pred is None:
            continue
        print("Sentence : {} predict : {} , actual : {}".format(sen, pred, label))
        if pred == -99:
            continue
        else:
            if pred == label:
                correct += 1
            total += 1

print("Threshold: " + str(threshold))
print("Acc: " + str(correct/total))
print("Correct: " + str(correct))
print("Total: " + str(total))

    # test_set, test_label = file_reader().read(path=test_direc)

    # print(model.similarity('story', 'plot'))
    # threshold += 0.05