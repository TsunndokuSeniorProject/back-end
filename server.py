from flask import Flask, jsonify, request
app = Flask(__name__)

temp_db_mutant = [{
    "id":"weapon-X",
    "name":"Logan Paul"
}]

@app.route('/api/1.0/test', methods=['GET'])
def get_test():
    return jsonify({'test': "this is an example"})

@app.route("/api/1.0/mutant", methods=['GET'])
def get_mutant():
    return jsonify(temp_db_mutant)

@app.route("/api/1.0/mutant", methods=['POST'])
def post_mutant():
    req = request.json
    if not req or not 'id' in req or not 'name' in req:
        return "something missing",400
    temp_db_mutant.append(req)
    return jsonify(temp_db_mutant)

if __name__=="__main__":
    app.run(port="5001")
