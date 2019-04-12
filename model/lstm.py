from keras.optimizers import Adam, RMSprop
from keras.layers import LSTM, Embedding, Dense, Input, GRU, Bidirectional
from keras import Model
from gensim.models.word2vec import Word2Vec
import os
import json
from keras.preprocessing.text import Tokenizer
import numpy as np
from keras.callbacks import ModelCheckpoint
import re
from keras.preprocessing.sequence import pad_sequences
from keras.utils.np_utils import to_categorical
import pandas as pd
import random
import tensorflow as tf
import sys
from sklearn.externals import joblib
from model.file_reader import file_reader

class lstm:
    def __init__(self):
        self.MAX_SEQUENCE_LENGTH = 40
        self.MAX_NB_WORDS = 20000
        self.EMBEDDING_DIM = 100
        self.VALIDATION_SPLIT = 0.1
        self.tokenizer = Tokenizer(num_words=25000)
        
    def tokenize(self, train_direc):
        with open(train_direc, 'r') as fp:
            data = fp.readlines()
        self.tokenizer.fit_on_texts(data)
        joblib.dump(self.tokenizer, './review_tokenizer.sav')

    def train(self, train_direc, epoch):
        
        train_set, raw_train_labels = file_reader().read_v2(train_direc, 1, 2)
        train_labels = []
        for label in raw_train_labels:
            if label == -1:
                train_labels.append(2)
            else:
                train_labels.append(label)
        self.tokenizer.fit_on_texts(train_set)
        joblib.dump(self.tokenizer, './review_tokenizer.sav')
        
        train_sequences = self.tokenizer.texts_to_sequences(train_set)
        # train_labels = to_categorical(np.asarray(train_labels))
        
        smt = Word2Vec.load('gensim_model.sav')
        
        word_index = self.tokenizer.word_index
        print('Number of Unique Tokens', len(word_index))

        data = pad_sequences(train_sequences, maxlen=self.MAX_SEQUENCE_LENGTH)
        
        labels = to_categorical(np.asarray(train_labels))
        print('Shape of Data Tensor:', data.shape)
        print('Shape of Label Tensor:', labels.shape)

        # indices = np.arange(data.shape[0])
        # np.random.shuffle(indices)
        # data = data[indices]
        # labels = labels[indices]
        
        # x_train = data[:-nb_validation_samples]
        # y_train = labels[:-nb_validation_samples]
        # x_val = data[-nb_validation_samples:]
        # y_val = labels[-nb_validation_samples:]

        print("Simplified LSTM neural network")
        self.model.summary()
        cp = ModelCheckpoint('model_lstm.hdf5',monitor='val_acc',verbose=1,save_best_only=True)
        history = self.model.fit(data, labels, validation_split=self.VALIDATION_SPLIT, epochs=epoch, batch_size=32,callbacks=[cp])


    def initialize_model(self, num_class, weight_direc=None):
        gensim_model = Word2Vec.load('./model/gensim_model.sav')
        
        self.tokenizer = joblib.load('./model/review_tokenizer.sav')
        word_index = self.tokenizer.word_index
        embeddings_index = {}
        if weight_direc is not None:
            f = open(weight_direc,encoding='utf8')
            for line in f:
                
                values = line.split()
                word = values[0]
                coefs = np.asarray(values[1:], dtype='float32')
                embeddings_index[word] = coefs
            f.close()

            print('Total %s word vectors in provided weight direc.' % len(embeddings_index))

            embedding_matrix = np.random.random((len(word_index) + 1, self.EMBEDDING_DIM))
            for word, i in word_index.items():
                embedding_vector = embeddings_index.get(word)
                if embedding_vector is not None:
                    # words not found in embedding index will be all-zeros.
                    embedding_matrix[i] = embedding_vector

            embeddings = Embedding(len(word_index) + 1,
                                    self.EMBEDDING_DIM,weights=[embedding_matrix],
                                    input_length=self.MAX_SEQUENCE_LENGTH, trainable=False)

        else:
            embeddings = Embedding(len(word_index) + 1, self.EMBEDDING_DIM, input_length=self.MAX_SEQUENCE_LENGTH, trainable=True)

        sequence_input = Input(shape=(self.MAX_SEQUENCE_LENGTH,), dtype='int32')
        embedded_sequences = embeddings(sequence_input)
        # embedded_sequences = gensim_model.wv.get_keras_embedding()(sequence_input)
        lstm_1 = Bidirectional(GRU(units=64, dropout=0.2, return_sequences=True))(embedded_sequences)
        lstm_last = Bidirectional(GRU(units=64, dropout=0.2))(lstm_1)
        output = Dense(num_class, activation='softmax')(lstm_last)

        self.model = Model(sequence_input, output)
    
    def compile_model(self, loss_function, optimizer):
        self.model.compile(loss=loss_function, optimizer=optimizer, metrics=['acc'])


    def test(self, test_direc):
        # read file
        test_set, raw_test_labels = file_reader().read_v2(test_direc, 1, 2)
        test_labels = []
        for label in raw_test_labels:
            if label == -1:
                test_labels.append(2)
            else:
                test_labels.append(label)


        test_sequences = self.tokenizer.texts_to_sequences(test_set)
        test_data = pad_sequences(test_sequences, maxlen=self.MAX_SEQUENCE_LENGTH)
        test_labels = to_categorical(np.asarray(test_labels))

		# evaluate using keras
        res = self.model.evaluate(test_data, test_labels)
        print(self.model.metrics_names)
        print(res)

	
    def load_weights(self, weight):
        self.model.load_weights(weight)
        print("weight loaded successfully")

    
    def predict(self, incoming_review):
        test_sequences = self.tokenizer.texts_to_sequences(incoming_review)
        test_data = pad_sequences(test_sequences, maxlen=self.MAX_SEQUENCE_LENGTH)

        res = self.model.predict(test_data)
        return res


if __name__ == '__main__':
    lstm = lstm()
    lstm.tokenize('C:/Users/USER/Downloads/neo_sentences_filtered.txt')
    lstm.initialize_model(num_class=3, weight_direc='gensim_vec.txt')
    lstm.compile_model(loss_function='categorical_crossentropy', optimizer=RMSprop(1e-4))
    lstm.train('C:/Users/USER/Downloads/test.txt', epoch=13)
    # lstm.test("C:/Users/USER/Downloads/test.txt")