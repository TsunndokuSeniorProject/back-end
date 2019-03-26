from keras.optimizers import Adam, RMSprop
from keras.layers import LSTM, Embedding, Dense, Input, Dropout, GRU
from keras import Model
import os
import json
from keras.preprocessing.text import Tokenizer
import csv
import numpy as np
from keras.callbacks import ModelCheckpoint
import re
from keras.preprocessing.sequence import pad_sequences
from keras.utils.np_utils import to_categorical
import pandas as pd
import random 
import sys
sys.path.append("../")
from web_scraper.goodreads.file_reader import file_reader

def clean_str(string):
    string = re.sub(r"\\", "", string)
    string = re.sub(r"\'", "", string)
    string = re.sub(r"\"", "", string)
    return string.strip().lower()


MAX_SEQUENCE_LENGTH = 40
MAX_NB_WORDS = 20000
EMBEDDING_DIM = 100
VALIDATION_SPLIT = 0.2

train_set = []
train_direc = "C:/Users/USER/Downloads/10000train.txt"

train_set, train_labels = file_reader().read(path=train_direc)

tokenizer = Tokenizer(num_words=25000)
tokenizer.fit_on_texts(train_set)

train_sequences = tokenizer.texts_to_sequences(train_set)
# train_labels = to_categorical(np.asarray(train_labels))


word_index = tokenizer.word_index
print('Number of Unique Tokens', len(word_index))


data = pad_sequences(train_sequences, maxlen=MAX_SEQUENCE_LENGTH)
labels = to_categorical(np.asarray(train_labels))
print('Shape of Data Tensor:', data.shape)
print('Shape of Label Tensor:', labels.shape)

indices = np.arange(data.shape[0])
np.random.shuffle(indices)
data = data[indices]
labels = labels[indices]
nb_validation_samples = int(VALIDATION_SPLIT * data.shape[0])

x_train = data[:-nb_validation_samples]
y_train = labels[:-nb_validation_samples]
x_val = data[-nb_validation_samples:]
y_val = labels[-nb_validation_samples:]

embeddings_index = {}
f = open('C:/Users/USER/Downloads/glove.6B/glove.6B.100d.txt',encoding='utf8')
for line in f:
    values = line.split()
    word = values[0]
    coefs = np.asarray(values[1:], dtype='float32')
    embeddings_index[word] = coefs
f.close()

print('Total %s word vectors in Glove 6B 100d.' % len(embeddings_index))

embedding_matrix = np.random.random((len(word_index) + 1, EMBEDDING_DIM))
for word, i in word_index.items():
    embedding_vector = embeddings_index.get(word)
    if embedding_vector is not None:
        # words not found in embedding index will be all-zeros.
        embedding_matrix[i] = embedding_vector

embedding_layer = Embedding(len(word_index) + 1,
                            EMBEDDING_DIM,weights=[embedding_matrix],
                            input_length=MAX_SEQUENCE_LENGTH, trainable=True)

sequence_input = Input(shape=(MAX_SEQUENCE_LENGTH,), dtype='int32')
embedded_sequences = embedding_layer(sequence_input)
# embeddings = Embedding(len(word_index) + 1, EMBEDDING_DIM, input_length=MAX_SEQUENCE_LENGTH, trainable=True)(sequence_input)
lstm_1 = GRU(units=64, dropout=0.2, return_sequences=True)(embedded_sequences)
lstm_last = GRU(units=64, dropout=0.2)(lstm_1)
output = Dense(3, activation='softmax')(lstm_last)

model = Model(sequence_input, output)
model.compile(loss='categorical_crossentropy', optimizer=RMSprop(1e-4), metrics=['acc'])

# model.load_weights('model_lstm.hdf5')

print("Simplified LSTM neural network")
model.summary()
cp=ModelCheckpoint('model_lstm.hdf5',monitor='val_acc',verbose=1,save_best_only=True)
history=model.fit(x_train, y_train, validation_data=(x_val, y_val), epochs=10, batch_size=32,callbacks=[cp])

test_set = []
test_direc = "C:/Users/USER/Downloads/test.txt"

test_set, test_labels = file_reader().read_v2(path=test_direc)

test_sequences = tokenizer.texts_to_sequences(test_set)
test_data = pad_sequences(test_sequences, maxlen=MAX_SEQUENCE_LENGTH)
test_labels = to_categorical(np.asarray(test_labels))

res = model.evaluate(test_data, test_labels)
print(model.metrics_names)
print(res)