from keras.optimizers import Adam
from keras.layers import LSTM, Embedding, Dense, Input, Dropout, Bidirectional, GRU
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

def clean_str(string):
    string = re.sub(r"\\", "", string)
    string = re.sub(r"\'", "", string)
    string = re.sub(r"\"", "", string)
    return string.strip().lower()


directory = "C:/Users/hpEnvy/Downloads/sentiment-analysis-on-movie-reviews/"


MAX_SEQUENCE_LENGTH = 1000
MAX_NB_WORDS = 20000
EMBEDDING_DIM = 100
VALIDATION_SPLIT = 0.2

texts = []
labels = []
with open(directory+'train.tsv') as tsvfile:
    reader = csv.DictReader(tsvfile, dialect='excel-tab')
    for row in reader:
      texts.append(list(row.values())[2])
      labels.append(list(row.values())[3])

tokenizer = Tokenizer(num_words=MAX_NB_WORDS)
tokenizer.fit_on_texts(texts)
sequences = tokenizer.texts_to_sequences(texts)

word_index = tokenizer.word_index
print('Number of Unique Tokens', len(word_index))

data = pad_sequences(sequences, maxlen=MAX_SEQUENCE_LENGTH)
labels = to_categorical(np.asarray(labels))
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

# embeddings_index = {}
# f = open('/kaggle/input/embeddings/glove.840B.300d/glove.840B.300d.txt', 'utf-8')
# for line in f:
#     values = line.split()
#     word = values[0]
#     coefs = np.asarray(values[1:], dtype='float32')
#     embeddings_index[word] = coefs
# f.close()

# print('Total %s word vectors in Glove 6B 100d.' % len(embeddings_index))

# embedding_matrix = np.random.random((len(word_index) + 1, EMBEDDING_DIM))
# for word, i in word_index.items():
#     embedding_vector = embeddings_index.get(word)
#     if embedding_vector is not None:
#         # words not found in embedding index will be all-zeros.
#         embedding_matrix[i] = embedding_vector

# embedding_layer = Embedding(len(word_index) + 1,
#                             EMBEDDING_DIM,weights=[embedding_matrix],
#                             input_length=MAX_SEQUENCE_LENGTH,trainable=True)

sequence_input = Input(shape=(MAX_SEQUENCE_LENGTH,), dtype='int32')
embedded_sequences = Embedding(len(word_index) + 1, EMBEDDING_DIM, input_length=MAX_SEQUENCE_LENGTH, trainable=True)(sequence_input)
# embedded_sequences = embedding_layer(sequence_input)
# lstm_1 = Bidirectional(LSTM(units=32, dropout=0.2, return_sequences=True))(embedded_sequences)
# lstm_last = Bidirectional(LSTM(units=32, dropout=0.2))(lstm_1)
gru_1 = GRU(32)(embedded_sequences)
drop = Dropout(0.2)(gru_1)
output = Dense(5,activation='softmax')(drop)

model = Model(sequence_input, output)
model.compile(loss='categorical_crossentropy', optimizer=Adam(1e-4), metrics=['acc'])

model.load_weights('model_gru.hdf5')
print("Simplified LSTM neural network")
model.summary()
cp=ModelCheckpoint('model_gru.hdf5',monitor='val_acc',verbose=1,save_best_only=True)
history=model.fit(x_train, y_train, validation_data=(x_val, y_val), epochs=5, batch_size=32,callbacks=[cp])
