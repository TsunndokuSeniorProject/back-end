from gensim.models import Word2Vec
from file_reader import file_reader
from gensim.test.utils import common_texts
from gensim.utils import simple_preprocess

train_set = []
train_direc = "C:/Users/USER/Downloads/10000train.txt"

train_set, train_labels = file_reader().read(path=train_direc)
processed = []
for sentence in train_set:
    processed.append(simple_preprocess(sentence))

model = Word2Vec(processed)

model.train(processed, total_examples=len(processed), epochs=10)

print(model.wv.most_similar(positive='narrative'))