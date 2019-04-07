from gensim.models import Word2Vec
from gensim.test.utils import common_texts
from gensim.utils import simple_preprocess, deaccent
import sys
sys.path.append("../")
from file_reader import file_reader
from oms import opinion_mining_system

train_set = []
train_direc = "C:/Users/USER/Downloads/sentences_filtered_jab.txt"

with open(train_direc, 'r', encoding='utf8') as f:
    data = f.readlines()
f.close()

processed = []
for sentence in data:
    processed.append(simple_preprocess(sentence))

model = Word2Vec(processed)

print("start training")
model.train(processed, total_examples=len(processed), epochs=10)
print("training finished")
# write = ''
# for word in model.wv.index2word:
#     write = write + " " + word


# with open("wvRes.text", 'w+', encoding='utf8') as fp:
#     fp.write(write)

print(model.wv.most_similar(positive='story'))
print(model.wv.most_similar(positive='character'))
print(model.wv.most_similar(positive='writing'))

test_set = []
test_direc = "C:/Users/USER/Downloads/test.txt"

test_set, test_label = file_reader().read(test_direc)

aspects = opinion_mining_system().operate_aspect_extraction(full_text_reviews=" ".join(test_set))


res = []
for sen in test_set:
    for aspect in aspects:
        if aspect[0].lower() in sen.lower():
            a = dict()
            try:
                a['story_sim'] = model.similarity('story', aspect[0].lower())
                a['char_sim'] = model.similarity('character', aspect[0].lower())
                a['writing_sim'] = model.similarity('writing', aspect[0].lower())
                max_sim = max(a.values())
                print(aspect[0].lower())
                if max_sim < 0.7:
                    res.append(-99)
                for asp, sim in a.items():
                    if max_sim == sim:
                        if asp == 'story_sim':
                            res.append(1)
                        elif asp == 'writing_sim':
                            res.append(2)
                        elif asp == 'char_sim':
                            res.append(3)
            except KeyError:
                res.append(-99)           

correct, total = 0, 0
for pred, label in zip(res, test_label):
    if pred == -99:
        continue
    else:
        if pred == label:
            correct += 1
        total += 1

print(correct/total)
print("Correct: " + str(correct))
print("Total: " + str(total))


# test_set, test_label = file_reader().read(path=test_direc)

# print(model.similarity('story', 'plot'))