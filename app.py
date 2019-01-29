from flask import Flask, jsonify, request
from model.model import Model
from datetime import datetime
import time
import os
import requests
from bs4 import BeautifulSoup
import nltk
nltk.download('punkt')


app = Flask(__name__)

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

@app.route('/api/1.0/test', methods=['GET'])
def get_test():
    return jsonify({'test': "this is an example"})

@app.route("/api/1.0/test/mutant", methods=['GET'])
def get_mutant():
    return jsonify(temp_db_mutant)

@app.route("/api/1.0/test/mutant", methods=['POST'])
def post_mutant():
    req = request.json
    if not req or not 'id' in req or not 'name' in req:
        return "something missing",400
    temp_db_mutant.append(req)
    return jsonify(temp_db_mutant)

@app.route("/api/1.0/predict", methods=['GET'])
def get_gender_predict():
    return jsonify(temp_db_predict)

@app.route("/api/1.0/predict/<int:id>", methods=['GET'])
def get_gender_predict_id(id):
    id = id-1
    if id > len(temp_db_predict):
        return "not found or invalid id",400
    else:
        return jsonify(temp_db_predict[id])

@app.route("/api/1.0/predict", methods=['POST'])
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

@app.route("/api/book/isbn/<string:isbn>", methods=['GET'])
def get_book(isbn):
    book_id = requests.get("https://www.goodreads.com/book/isbn_to_id?key=ZpKMgjJRKh5Gl7kV9PPUMg&isbn="+isbn)

    if len(book_id.text) is not 0:
        res = requests.get("https://www.goodreads.com/book/show/"+book_id.text)

        if str(res.status_code) == "200":

            soup = BeautifulSoup(res.text,'html.parser')

            reviews = soup.find_all('div', {'class': 'reviewText stacked'})

            name = soup.find_all('h1', {'itemprop': 'name'})

            name = str(name[0].text).strip()

            book_reviews = {
                'ID': book_id.text,
                'Name': name,
                'Reviews':[]
            }

            for review in reviews:
                texts = review.find_all("span", id=lambda value: value and value.startswith("freeTextContainer"))
                for text in texts:
                    book_reviews['Reviews'].append({"Review": text.text})

            return jsonify(book_reviews)

        else:
            return jsonify({"fail_message":"couldn't connect to goodreads, try again later."})

    return jsonify({"fail_message":"couldn't find book by the given isbn."})



@app.route("/api/book/nltk/", methods=['GET'])
def get_nltk():
    s = "aaa milk is"
    token = nltk.word_tokenize(s)
    token = nltk.pos_tag(token)
    return jsonify({"fail_message":token})


if __name__=="__main__":
    model = Model().loadModelState('model/state/model_state.sav')
    port = int(os.environ.get('PORT', 33507))
    app.run(debug=True, port=port)

