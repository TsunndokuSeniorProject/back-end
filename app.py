from flask import Flask, jsonify, request
from keras.optimizers import Adam, RMSprop
from model.lstm import lstm
from model.gensim_w2v import gensim_w2v
import model.text_processor as text_processor
import web_scraper.goodreads.scraper as scraper
from datetime import datetime
import time
import os
import requests
from bs4 import BeautifulSoup
import nltk
import re
import json
import pymongo
import pandas as pd
import numpy as np
import tensorflow as tf

app = Flask(__name__)

uri = "mongodb://tsundoku_db:tsundoku_db_007@ds133875.mlab.com:33875/tsundoku"

client = pymongo.MongoClient(uri)

db = client.get_default_database()

books = db['Books']


@app.route('/', methods=['GET'])
def welcome():
    return jsonify({'acknowledge': "welcome to Tsun-Do-Ku api"})


####### Production API #######

@app.route("/api/book/isbn/<string:isbn>", methods=['GET'])
def get_review_by_isbn(isbn):
    book_id = requests.get("https://www.goodreads.com/book/isbn_to_id?key=ZpKMgjJRKh5Gl7kV9PPUMg&isbn="+isbn)
    if len(book_id.text) is not 0:
        book_reviews = scraper.get_book_reviews(book_id.text)
        return jsonify(book_reviews)
    return jsonify({"fail_message":"couldn't find book by the given isbn."})

def find_max(np_list):
    result = []
    for np_item in np_list:
        result.append(np.argmax(np_item))
    return result
@app.route("/api/book/isbn/interpret/<string:isbn>", methods=['GET'])
def get_review_by_isbn_with_predict_result(isbn):
    
    book_id = requests.get("https://www.goodreads.com/book/isbn_to_id?key=ZpKMgjJRKh5Gl7kV9PPUMg&isbn="+isbn)
    if len(book_id.text) is not 0:
        book_reviews = scraper.get_book_reviews(book_id.text)
        if not("fail_message" in book_reviews):
            text = ""
            for review in book_reviews['Reviews']:
                text += review['Review'] + " "
            print(book_reviews["Author"])
            text = text_processor.replace_author(text, book_reviews["Author"])
            text = text_processor.replace_bookname(text, book_reviews["Name"])
            sentences_list = text_processor.split_into_sentences(text)
            sentences_list = text_processor.filter_english(sentences_list)

            aspect_res = aspect_gensim.predict(sentences_list)

            global graph
            with graph.as_default():
                result = np.asarray(polarity_lstm.predict(sentences_list))
            result = find_max(result)
            result = pd.DataFrame({"sentences": sentences_list, "aspect": aspect_res, "polarity": result})
            result = result.to_dict("records")
            book_reviews['sentiment'] = result
            return jsonify(book_reviews)
    return jsonify({"fail_message":"couldn't find book by the given isbn."})

@app.route("/api/book/id/interpret/<string:id>", methods=['GET'])
def get_review_by_id_with_predict_result(id):
    book_info = books.find_one({"_id":str(id)})
    if book_info is not None and book_info["Reviews"] != []:
        book_reviews = book_info
        text = ""
        for review in book_reviews['Reviews']:
            text += review['Review'] + " "

        text = text_processor.replace_author(text, book_reviews["Author"])
        text = text_processor.replace_bookname(text, book_reviews["Name"])
        sentences_list = text_processor.split_into_sentences(text)
        sentences_list = text_processor.filter_english(sentences_list)

        aspect_res = aspect_gensim.predict(sentences_list)
        
        global graph
        with graph.as_default():
            result = np.asarray(polarity_lstm.predict(sentences_list))
        result = find_max(result)
        result = pd.DataFrame({"sentences": sentences_list, "aspect": aspect_res, "polarity": result})
        result = pd.DataFrame({"sentences": sentences_list})
        result = result.to_dict("records")
        book_reviews['sentiment'] = result
        return jsonify(book_reviews)
    return jsonify({"fail_message":"couldn't find book by the given id."})


@app.route("/api/testML", methods=['GET'])
def testML():
    sentences_list = ["I hope for each and every time I pick up a book", "I love twilight", "She travels to her clients instead of them coming to her", "But then she overhears a voicemail message one of the women plays"]
    aspect_gensim = gensim_w2v()
    aspect_res = aspect_gensim.predict(sentences_list)
    
    global graph
    with graph.as_default():
        result = np.asarray(polarity_lstm.predict(sentences_list))
    result = find_max(result)
    result = pd.DataFrame({"sentences": sentences_list, "aspect": aspect_res, "polarity": result})
    result = pd.DataFrame({"sentences": sentences_list})
    result = result.to_dict("records")
    book_reviews = result
    return jsonify(book_reviews)

@app.route("/api/book/id/<string:id>", methods=['GET'])
def get_book_by_id(id):
    query = books.find_one({"_id":str(id)})
    
    return jsonify({"book_by_id":query})


@app.route("/api/all_books/list", methods=['GET'])
def get_books_list():
    query = books.find({}, {"_id":1, "Name":1, "Genre":1})
    all_info = []
    for doc in query:
        all_info.append(doc)
    return jsonify({"all_books":all_info})

@app.route("/api/book/all_books/genre/<string:genre>", methods=['GET'])
def get_book_by_genre(genre):
    query = books.find({"Genre":genre.capitalize()})
    all_info = []
    for doc in query:
        all_info.append(doc)
    return jsonify({"all_books_in_genre":all_info})

@app.route("/api/book/all_books/", methods=['GET'])
def get_all_books():
    
    query = books.find().limit(50)
    all_info = []
    for doc in query:
        all_info.append(doc)
    return jsonify({"all_books_in_genre":all_info})

if __name__=="__main__":
    aspect_gensim = gensim_w2v()
    polarity_lstm = lstm()
    
    # fix for tensor not element of graph error -- the graph variable will be use at the predict() function
    graph = tf.get_default_graph()

    polarity_lstm.initialize_model(num_class=3, weight_direc="./model/vectors/gensim_vec.txt")
    polarity_lstm.compile_model(loss_function='categorical_crossentropy', optimizer=Adam())
    polarity_lstm.load_weights('./model/model_lstm.hdf5')
    port = int(os.environ.get('PORT', 33507))
    app.run(debug=True, port=port)