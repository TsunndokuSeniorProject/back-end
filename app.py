from flask import Flask, jsonify, request
from model.model import Model
from model.subjectivity_model import SVM_subjectivity
from model.word_feature import word_feature, sentence_selector
import model.imitation_of_oms as oms
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
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

app = Flask(__name__)

uri = "mongodb://tsundoku_db:tsundoku_db_007@ds133875.mlab.com:33875/tsundoku"

client = pymongo.MongoClient(uri)

db = client.get_default_database()

books = db['Books']

####### Testing API #######

temp_db_mutant = [{
    "id":"weapon-X",
    "name":"Logan Paul"
}]
temp_db_predict = [{
    "id":1,
    "height":68,
    "weight":97,
    "predicted_gender": "ApacheHelicopter",
}]

@app.route('/', methods=['GET'])
def welcome():
    return jsonify({'acknowledge': "welcome to Tsun-Do-Ku api"})

@app.route('/api/test', methods=['GET'])
def get_test():
    return jsonify({'test': "this is an example"})

@app.route("/api/test/mutant", methods=['GET'])
def get_mutant():
    return jsonify(temp_db_mutant)

@app.route("/api/test/mutant", methods=['POST'])
def post_mutant():
    req = request.json
    if not req or not 'id' in req or not 'name' in req:
        return "something missing",400
    temp_db_mutant.append(req)
    return jsonify(temp_db_mutant)

@app.route("/api/test/predict", methods=['GET'])
def get_gender_predict():
    return jsonify(temp_db_predict)

@app.route("/api/test/predict/<int:id>", methods=['GET'])
def get_gender_predict_id(id):
    id = id-1
    if id > len(temp_db_predict):
        return "not found or invalid id",400
    else:
        return jsonify(temp_db_predict[id])

@app.route("/api/test/predict", methods=['POST'])
def post_gender_predict():
    req = request.json
    if not req or not 'height' in req or not 'weight' in req:
        return "something missing",400
    predit_result = model.predict([[req['height'], req['weight']]])
    temp_db_predict.append({
        "id":len(temp_db_predict)+1,
        "height":req['height'],
        "weight":req['weight'],
        "predicted_gender":predit_result[0]
    })
    return jsonify(temp_db_predict)


####### Production API #######

@app.route("/api/book/isbn/<string:isbn>", methods=['GET'])
def get_review_by_isbn(isbn):
    book_id = requests.get("https://www.goodreads.com/book/isbn_to_id?key=ZpKMgjJRKh5Gl7kV9PPUMg&isbn="+isbn)
    if len(book_id.text) is not 0:
        book_reviews = scraper.get_book_reviews(book_id.text)
        return jsonify(book_reviews)
    return jsonify({"fail_message":"couldn't find book by the given isbn."})

@app.route("/api/book/isbn2/<string:isbn>", methods=['GET'])
def get_review_by_isbn_with_predict_result(isbn):
    
    book_id = requests.get("https://www.goodreads.com/book/isbn_to_id?key=ZpKMgjJRKh5Gl7kV9PPUMg&isbn="+isbn)
    if len(book_id.text) is not 0:
        book_reviews = scraper.get_book_reviews(book_id.text)
        if not("fail_message" in book_reviews):
            text = ""
            for review in book_reviews['Reviews']:
                text += review['Review'] + " "
            word_processor = word_feature()
            word_feature_list, word_map, all_reviews_sentence = word_processor.create_word_feature_test_set(text)
            selector = sentence_selector()
            svm = SVM_subjectivity()
            svm.loadModelState('model/state/subjectivity_model_state.sav')
            subjectivity_word = svm.test(word_feature_list,word_map)

            filtered_sentence = selector.filter(all_reviews_sentence, subjectivity_word)
            filtered_sentence = ". ".join(filtered_sentence)
            filtered_sentence = filtered_sentence.replace("\n"," ").replace(".",". ")
            filtered_sentence = re.sub(r'[^\x00-\x7F]+','', filtered_sentence)
            a = oms.preProcessing(filtered_sentence)
            b = oms.tokenizeReviews(a)
            c = oms.posTagging(b)
            d = oms.aspectExtraction(c)
            result = oms.identifyOpinionWords(c, d)
            book_reviews['sentiment'] = result
            return jsonify(book_reviews)
    return jsonify({"fail_message":"couldn't find book by the given isbn."})

@app.route("/api/book/<string:id>", methods=['GET'])
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
    model = Model().loadModelState('model/state/model_state.sav')
    
    
    port = int(os.environ.get('PORT', 33507))
    app.run(debug=True, port=port)

