from keras import models
from keras import layers
from keras import optimizers
import keras
import json
# This Keras model class is not complete, but can be compile with no error

max_chr = 10000

review = ""
with open('../web_scraper/novel/comments/review_006246616X.json', 'r') as fp:
    data = json.load(fp)
    for comment in data['Comment']:
        print(comment['Review'])
        review = review+comment['Review']

#Tokenize review
tokenizer = keras.preprocessing.text.Tokenizer(num_words=10000)
tokenizer.fit_on_texts(texts=review)
dictionary = tokenizer.word_index

# Change text to the token create by tokenizer i.e hello changed to token '1'
sequences = tokenizer.texts_to_sequences(review)
sequences = keras.preprocessing.sequence.pad_sequences(sequences)

# 1 represent positive, 0 represent negative
label = [1, 0]

# Initialize the model and add LSTM layer and output as Dense Layer
model = models.Sequential()
model.add(layers.Embedding(input_dim=max_chr, output_dim=32))
model.add(layers.LSTM(units=32, dropout=0.2))
model.add(layers.Dense(units=2, activation="sigmoid"))

# Using adam optimizer as it gives the best performance in deceptive reviews work, can be change later
model.compile(loss='sparse_categorical_crossentropy',
              optimizer=optimizers.adam(lr=0.01),
              metrics=['accuracy'])
# Fit model with mock data for five epoch
model.fit(x=sequences, y=label, batch_size=5, epochs=5)
print(model.evaluate(x=sequences, y=label))
