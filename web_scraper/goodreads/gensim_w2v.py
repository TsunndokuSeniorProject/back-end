from gensim.models import Word2Vec
from file_reader import file_reader
from gensim.test.utils import common_texts
from gensim.utils import simple_preprocess

train_set = []
train_direc = "C:/Users/USER/Downloads/10000train.txt"

train_set, train_labels = file_reader().read(path=train_direc)

processed = simple_preprocess(train_set)

model = Word2Vec(sentences=train_set)

model.train(train_set, total_examples=model.corpus_count, epochs=5)
