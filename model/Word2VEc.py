from keras.models import Model
from keras.layers import Input, Dense, Reshape, merge
from keras.layers.embeddings import Embedding
from keras.preprocessing import sequence
from keras.utils import generic_utils
from keras import optimizers
import collections
import spacy
import os
import zipfile
import numpy as np
import tensorflow as tf
import json
import keras
from urllib import request
from keras.callbacks import History 



def read_my_data(directory):
    for file in directory:
        with open(directory+file, 'r') as fp:
            data = json.load(fp)



def maybe_download(filename, url, expected_bytes):
    """Download a file if not present, and make sure it's the right size."""
    if not os.path.exists(filename):
        filename, _ = request.urlretrieve(url + filename, filename)
    statinfo = os.stat(filename)
    if statinfo.st_size == expected_bytes:
        print('Found and verified', filename)
    else:
        print(statinfo.st_size)
        raise Exception(
            'Failed to verify ' + filename + '. Can you get to it with a browser?')
    return filename


# Read the data into a list of strings.
def read_data(filename):
    """Extract the first file enclosed in a zip file as a list of words."""
    with zipfile.ZipFile(filename) as f:
        data = tf.compat.as_str(f.read(f.namelist()[0])).split()
    return data


def build_dataset(words, n_words):
    """Process raw inputs into a dataset."""
    count = [['UNK', -1]]
    count.extend(collections.Counter(words).most_common(n_words - 1))
    dictionary = dict()
    for word, _ in count:
        dictionary[word] = len(dictionary)
    data = list()
    unk_count = 0
    for word in words:
        if word in dictionary:
            index = dictionary[word]
        else:
            index = 0  # dictionary['UNK']
            unk_count += 1
        data.append(index)
    count[0][1] = unk_count
    reversed_dictionary = dict(zip(dictionary.values(), dictionary.keys()))
    return data, count, dictionary, reversed_dictionary


def collect_data(vocabulary_size=10000):
    url = 'http://mattmahoney.net/dc/'
    filename = maybe_download('text8.zip', url, 31344016)
    vocabulary = read_data(filename)
    print(vocabulary[:7])
    data, count, dictionary, reverse_dictionary = build_dataset(vocabulary,
                                                                vocabulary_size)
    del vocabulary  # Hint to reduce memory.
    return data, count, dictionary, reverse_dictionary


# function to test model
def test_model(data_path, vocab_size):
    model, validation_model = initialize_model(vocab_size, 300)
    reviews = []
    for file in os.listdir(data_path):
        with open(data_path+file, 'r') as fp:
            data = json.load(fp)
            fp.close()
            
            for review in data['Reviews']:
                for single in review['Review']:
                    
                    reviews.append(single)
    tokenizer = keras.preprocessing.text.Tokenizer()
    tokenizer.fit_on_texts(reviews)
    sequences = tokenizer.texts_to_sequences(reviews)
    new_sequences = []
    sampling_table = sequence.make_sampling_table(vocab_size)
    for seq in sequences:
        if type(seq) == list:
            if len(seq) > 0:
                new_sequences.append(seq[0])
        else:
            new_sequences.append(seq)
    couples, labels = keras.preprocessing.sequence.skipgrams(new_sequences, vocab_size, sampling_table=sampling_table)
    model.load_weights("C:/Users/USER/Back-end/model/word2vec_weight.h5")
    word_target, word_context = zip(*couples)
    word_target = np.array(word_target, dtype="int32")
    word_context = np.array(word_context, dtype="int32")
    result = model.test_on_batch([word_target, word_context],labels)
    print(result)

def train_model(data_path, vocab_size, num_epochs):
    model, validation_model = initialize_model(vocab_size, 300)
    reviews = []
    history = History()

    for file in os.listdir(data_path):
        with open(data_path+file, 'r') as fp:
            data = json.load(fp)
            fp.close()
            
            for review in data['Reviews']:
                for single in review['Review']:
                    
                    reviews.append(single)
    tokenizer = keras.preprocessing.text.Tokenizer()
    tokenizer.fit_on_texts(reviews)
    sequences = tokenizer.texts_to_sequences(reviews)
    new_sequences = []
    sampling_table = sequence.make_sampling_table(vocab_size)
    for seq in sequences:
        if type(seq) == list:
            if len(seq) > 0:
                new_sequences.append(seq[0])
        else:
            new_sequences.append(seq)
    couples, labels = keras.preprocessing.sequence.skipgrams(new_sequences, vocab_size, sampling_table=sampling_table)
    word_target, word_context = zip(*couples)
    word_target = np.array(word_target, dtype="int32")
    word_context = np.array(word_context, dtype="int32")
    history = model.fit([word_target, word_context], labels, epochs=100, callbacks=[history], validation_split=0.33   )
    model.save_weights("word2vec_weights.h5")
    print(history.history)



def initialize_model(vocab_size, vector_dim):
    # create some input variables
    input_target = Input((1,))
    input_context = Input((1,))

    embedding = Embedding(vocab_size, vector_dim, input_length=1, name='embedding')
    target = embedding(input_target)
    target = Reshape((vector_dim, 1))(target)
    context = embedding(input_context)
    context = Reshape((vector_dim, 1))(context)

    # setup a cosine similarity operation which will be output in a secondary model
    similarity = merge.dot(inputs = [target, context], normalize=True, axes=0)
    # similarity = merge([target, context], mode='cos', dot_axes=0)

    # now perform the dot product operation to get a similarity measure
    # dot_product = merge.Dot(normalize=False, axes=1)
    dot_product = merge.dot(inputs = [target, context], axes = 1, normalize=False)
    dot_product = Reshape((1,))(dot_product)
    # add the sigmoid output layer
    output = Dense(1, activation='sigmoid')(dot_product)
    # create the primary training model
    # model = Model(input_shape=[input_target, input_context], output=output)
    model = Model(input=[input_target, input_context], output=output)
    model.compile(loss='binary_crossentropy', optimizer=optimizers.Adam(lr=0.001))
    # create a secondary validation model to run our similarity checks during training
    # validation_model = Model(input_shape=[input_target, input_context], output=similarity)
    validation_model = Model(input=[input_target, input_context], output=similarity)
    return model, validation_model



vocab_size = 10000

train_model("C:/Users/USER/Downloads/romance-20190204T074007Z-001/romance/", vocab_size, 100000)
test_model("C:/Users/USER/Downloads/romance-20190204T074007Z-001/romance/", 10000)

# data, count, dictionary, reverse_dictionary = collect_data(vocabulary_size=vocab_size)
# print(data[:7])



# window_size = 3
# vector_dim = 300
# epochs = 110100
# valid_size = 16  # Random set of words to evaluate similarity on.
# valid_window = 100  # Only pick dev samples in the head of the distribution.
# valid_examples = np.random.choice(valid_window, valid_size, replace=False)

# sampling_table = keras.preprocessing.sequence.make_sampling_table(vocab_size)
# couples, labels = keras.preprocessing.sequence.skipgrams(data, vocab_size, window_size=window_size,
#                                                          sampling_table=sampling_table)
                                                         
# X = np.array(couples, dtype="int32")

# print(couples[:10], labels[:10])

# model, validation_model = initialize_model(vocab_size, 300)


# class SimilarityCallback:
#     def run_sim(self):
#         for i in range(valid_size):
#             valid_word = reverse_dictionary[valid_examples[i]]
#             top_k = 8  # number of nearest neighbors
#             sim = self._get_sim(valid_examples[i])
#             nearest = (-sim).argsort()[1:top_k + 1]
#             log_str = 'Nearest to %s:' % valid_word
#             for k in range(top_k):
#                 close_word = reverse_dictionary[nearest[k]]
#                 log_str = '%s %s,' % (log_str, close_word)
#             print(log_str)

#     @staticmethod
#     def _get_sim(valid_word_idx):
#         sim = np.zeros((vocab_size,))
#         in_arr1 = np.zeros((1,))
#         in_arr2 = np.zeros((1,))
#         in_arr1[0,] = valid_word_idx
#         for i in range(vocab_size):
#             in_arr2[0,] = i
#             out = validation_model.predict_on_batch([in_arr1, in_arr2])
#             sim[i] = out
#         return sim


# sim_cb = SimilarityCallback()

# arr_1 = np.zeros((1,))
# arr_2 = np.zeros((1,))
# arr_3 = np.zeros((1,))
# for cnt in range(epochs):
#     idx = np.random.randint(0, len(labels)-1)
#     arr_1[0,] = word_target[idx]
#     arr_2[0,] = word_context[idx]
#     arr_3[0,] = labels[idx]
#     loss = model.train_on_batch([arr_1, arr_2], arr_3)
#     if cnt % 100 == 0:
#         print("Iteration {}, loss={}".format(cnt, loss))
#     if cnt % 10000 == 0:
#         sim_cb.run_sim()

# model.save(filepath="word2vec_model.h5")
# model.save_weights(filepath="word2vec_weight.h5")