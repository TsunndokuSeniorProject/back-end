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

st = "This is a cat, <imp_character> loves him very much."
print(simple_preprocess(st))

processed = []
for sentence in data:
    processed.append(simple_preprocess(sentence))

model = Word2Vec(processed)

model.train(processed, total_examples=len(processed), epochs=5)

# write = ''
# for word in model.wv.index2word:
#     write = write + " " + word


# with open("wvRes.text", 'w+', encoding='utf8') as fp:
#     fp.write(write)

# print(model.wv.most_similar(positive='<Character>'))

test_set = []
test_direc = "C:/Users/USER/Downloads/test.txt"

test_set, test_label = file_reader().read(test_direc)

aspects = opinion_mining_system().operate_aspect_extraction(full_text_reviews=" ".join(data))

print(aspects)

for sen in test_set:
    for aspect in aspects[0]:
        if aspect in sen:
            try:
                if model.similarity('story', aspect.lower()) >= 0.7:
                    story_sim = model.similarity('story', aspect)
                if model.similarity('character', aspect) >= 0.7:
                    char_sim = model.similarity('character', aspect)
                if model.similarity('writing', aspect) >= 0.7:
                    writing_sim = model.similarity('writing', aspect)
                aspect_sim = max(story_sim, char_sim, writing_sim)
            except KeyError:
                print("no word in this place")


# test_set, test_label = file_reader().read(path=test_direc)

# print(model.similarity('story', 'plot'))