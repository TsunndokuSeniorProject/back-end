from flask import Flask, jsonify, request
from model.model import Model
from datetime import datetime
import time


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

if __name__=="__main__":
    model = Model().loadModelState('model/state/model_state.sav')

    app.run()

