from flask import Flask, jsonify, request
from keras.optimizers import Adam, RMSprop
from model.lstm import lstm
from model.gensim_w2v import gensim_w2v
import model.text_processor as text_processor
import web_scraper.goodreads.scraper as scraper
from model.aggregator import compute_score
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
import datetime
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('stopwords')
# nltk.download('wordnet')
# nltk.download('sentiwordnet')

app = Flask(__name__)

uri = "mongodb://tsundoku_db:tsundoku_db_007@ds133875.mlab.com:33875/tsundoku"

client = pymongo.MongoClient(uri)

db = client.get_default_database()

books = db['Books']

graph = tf.get_default_graph()

aspect_gensim = gensim_w2v()

polarity_lstm = lstm()

# fix for tensor not element of graph error -- the graph variable will be use at the predict() function

polarity_lstm.initialize_model(num_class=3, weight_direc="./model/vectors/gensim_vec.txt")
polarity_lstm.compile_model(loss_function='categorical_crossentropy', optimizer=Adam(1e-4))
polarity_lstm.load_weights('./model/model_lstm.hdf5')


def find_max(np_list):
    result = []
    for np_item in np_list:
        result.append(np.argmax(np_item))
    return result

@app.route('/', methods=['GET'])
def welcome():
    return jsonify({'acknowledge': "welcome to Tsun-Do-Ku api"})

@app.route("/api/book/isbn/<string:isbn>", methods=['GET'])
def get_review_by_isbn(isbn):
    book_id = requests.get("https://www.goodreads.com/book/isbn_to_id?key=ZpKMgjJRKh5Gl7kV9PPUMg&isbn="+isbn)
    if len(book_id.text) is not 0:
        book_reviews = scraper.get_book_reviews(book_id.text)
        return jsonify(book_reviews)
    return jsonify({"fail_message":"couldn't find book by the given isbn."})

@app.route("/api/book/isbn/interpret/<string:isbn>", methods=['GET'])
def get_review_by_isbn_with_predict_result(isbn):
    # print(datetime.datetime.now())
    # print("start")
    book_id = requests.get("https://www.goodreads.com/book/isbn_to_id?key=ZpKMgjJRKh5Gl7kV9PPUMg&isbn="+isbn)
    if len(book_id.text) is not 0:
        book_reviews = scraper.get_book_reviews(book_id.text)
        if not("fail_message" in book_reviews):
            text = ""
            for review in book_reviews['Reviews']:
                text += review['Review'] + " "
            
            # print(book_reviews["Author"])
            # print(datetime.datetime.now())
            print("consolidate review")
            text = text_processor.replace_author(text, book_reviews["Author"])
            # print(datetime.datetime.now())
            # print("replace author")
            text = text_processor.replace_bookname(text, book_reviews["Name"])
            # print(datetime.datetime.now())
            # print("replace bookname")

            # text = text_processor.tag_character(text)

            # print(datetime.datetime.now())
            # print("replace impchar")
            sentences_list = text_processor.split_into_sentences_regex(text)
            # print(datetime.datetime.now())
            # print("split")
            sentences_list = text_processor.filter_english(sentences_list)
            # print(datetime.datetime.now())
            # print("fiter and stop word")
            global aspect_res
            aspect_res = aspect_gensim.predict(sentences_list)
            global graph, polarity_lstm        
            polar_res = []
            with graph.as_default():
                polar_res = polarity_lstm.predict(sentences_list)
                result = np.asarray(polar_res)
            result = find_max(result)
            book_reviews['sentiment'] = compute_score(aspect_res, result)
            result = pd.DataFrame({"sentences": sentences_list, "aspect": aspect_res, "polarity": result})
            result = result.to_dict("records")
            book_reviews['analysis'] = result
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

        print(book_reviews["Author"])
        # print(datetime.datetime.now())
        # print("consolidate review")
        text = text_processor.replace_author(text, book_reviews["Author"])
        # print(datetime.datetime.now())
        # print("replace author")
        text = text_processor.replace_bookname(text, book_reviews["Name"])
        # print(datetime.datetime.now())
        # print("replace bookname")

        # text = text_processor.tag_character(text)

        # print(datetime.datetime.now())
        # print("replace impchar")
        sentences_list = text_processor.split_into_sentences_regex(text)
        # print(datetime.datetime.now())
        # print("split")
        sentences_list = text_processor.filter_english(sentences_list)
        # print(datetime.datetime.now())
        # print("fiter and stop word")
        global aspect_res
        aspect_res = aspect_gensim.predict(sentences_list)
        global graph, polarity_lstm
        polar_res = []
        with graph.as_default():
            polar_res = polarity_lstm.predict(sentences_list)
            result = np.asarray(polar_res)
        result = find_max(result)
        book_reviews['sentiment'] = compute_score(aspect_res, result)
        result = pd.DataFrame({"sentences": sentences_list, "aspect": aspect_res, "polarity": result})
        result = result.to_dict("records")
        book_reviews['analysis'] = result
        
        return jsonify(book_reviews)
    return jsonify({"fail_message":"couldn't find book by the given id."})


@app.route("/api/testML", methods=['GET'])
def testML():
    sentences_list = ["I hope for each and every time I pick up a book", "I love twilight", "She travels to her clients instead of them coming to her", "But then she overhears a voicemail message one of the women plays"]
    global aspect_res
    aspect_res = aspect_gensim.predict(sentences_list)
    
    global graph, polarity_lstm
    with graph.as_default():
        result = np.asarray(polarity_lstm.predict(sentences_list))
    result = find_max(result)
    result = pd.DataFrame({"sentences": sentences_list, "aspect": aspect_res, "polarity": result})
    result = result.to_dict("records")
    book_reviews = result
    return jsonify(book_reviews)

@app.route("/api/book/id/<string:id>", methods=['GET'])
def get_book_by_id(id):
    query = books.find_one({"_id":str(id)})
    return jsonify({"book_by_id":query})

@app.route("/api/book/name/<string:name>", methods=['GET'])
def get_book_by_name(name):
    regx = re.compile(str(name), re.IGNORECASE)
    query = books.find({"Name":regx})
    book_found = []
    count = 0
    for item in query:
        count += 1
        book_found.append(item)
    if len(book_found) == 0:
        return jsonify({"all_book_found":"not found any books", "Hit":count})
    return jsonify({"all_book_found":book_found, "Hit":count})

@app.route("/api/all_books/list", methods=['GET'])
def get_books_list():
    query = books.find({}, {"_id":1, "Name":1, "Genre":1})
    all_info = []
    for doc in query:
        all_info.append(doc)
    return jsonify({"all_books":all_info})

@app.route("/api/book/all_books/genre/<string:genre>/<int:start>:<int:end>", methods=['GET'])
def get_book_by_genre(genre, start=0, end=10):
    regx = re.compile(str(genre), re.IGNORECASE)
    query = books.find({"Genre":regx}).skip(start).limit(end)
    all_info = []
    for doc in query:
        all_info.append(doc)
    return jsonify({"all_books_in_genre":all_info})

@app.route("/api/book/all_books/", methods=['GET'])
def get_all_books():
    
    query = books.find().limit(100)
    all_info = []
    for doc in query:
        all_info.append(doc)
    return jsonify({"all_books":all_info})

@app.route("/api/book/range_books/<int:start>:<int:end>", methods=['GET'])
def get_books_from_to(start, end):
    
    query = books.find().skip(start).limit(end)
    all_info = []
    for doc in query:
        all_info.append(doc)
    return jsonify({"books":all_info})

@app.route("/api/all_genre/", methods=['GET'])
def get_all_genre():
    query = books.distinct( "Genre" )
    return jsonify({"all_genre":query})


if __name__=="__main__":
    

    port = int(os.environ.get('PORT', 33507))
    # port = 8000
    app.run(debug=True, port=port)