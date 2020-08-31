from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbreview


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/save', methods=['POST'])
def post_article():
    city_receive = request.form['city_give']
    image_receive = request.form['image_give']
    when_receive = request.form['when_give']
    memo_receive = request.form['memo_give']

    doc = {
        'city': city_receive,
        'image': image_receive,
        'when': when_receive,
        'memo': memo_receive
    }

    db.mycity.insert_one(doc)

    return jsonify({'result': 'success', 'msg': '저장 완료!'})


@app.route('/show', methods=['GET'])
def read_articles():
    mycities = list(db.mycity.find({},{'_id':False}))
    return jsonify({'result': 'success', 'mycities': mycities})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)