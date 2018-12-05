from keras import models
from keras import layers
from keras import optimizers
import keras
import os
import json
# This Keras model class is not complete, but can be compile with no error

max_chr = 10000
directory = "../web_scraper/novel/comments/"
polar_label = []
review = []
i = 1
for file in os.listdir(directory):
    print(directory+file)
    with open(directory + file, 'r') as fp:
        data = json.load(fp)
        for comment in data['Comment']:
            review.append(comment['Review'])
            polar_label.append(comment['positivity'])
            i = i + 1
print(polar_label)

# Tokenize review
tokenizer = keras.preprocessing.text.Tokenizer(num_words=10000)
tokenizer.fit_on_texts(texts=review)
dictionary = tokenizer.word_index

# Change text to the token create by tokenizer i.e hello changed to token '1'
sequences = tokenizer.texts_to_sequences(review)
sequences = keras.preprocessing.sequence.pad_sequences(sequences)


# Initialize the model and add LSTM layer and output as Dense Layer
model = models.Sequential()
model.add(layers.Embedding(input_dim=max_chr, output_dim=32))
model.add(layers.LSTM(units=32, dropout=0.2))
model.add(layers.Dense(units=2, activation="sigmoid"))

# Using adam optimizer as it gives the best performance in deceptive reviews work, can be change later
model.compile(loss='sparse_categorical_crossentropy',
              optimizer=optimizers.adam(lr=0.01),
              metrics=['accuracy'])

model.fit(x=sequences, y=polar_label, epochs=5)
model.save_weights("polarity_weight.h5")
model.load_weights("polarity_weight.h5")
print(model.evaluate(x=sequences, y=polar_label))
