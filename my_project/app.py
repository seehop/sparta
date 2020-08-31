from pymongo import MongoClient
from flask import Flask, render_template, jsonify, request
import csv
from datetime import datetime
import init_db
import random
import schedule

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbsparta


# HTML 화면 보여주기
@app.route('/')
def home():
    return render_template('index.html')


#######DB에 있는 정보 중 조건에 맞는 애만 몇 개 랜덤으로 골라 사용자한테 보여주기
@app.route('/api/list', methods=['GET'])
def recommend_stocks():
    ###################### 1. db에서 stock 목록 전체를 검색합니다. ID는 제외하고 eper이 iper보다 낮고 pbr가 1.5보다 낮은 목록에서 3개를 랜덤 추출합니다.
    recommended_stocks = list(db.stocks.find({"$where": "this.eper < this.iper && this.pbr >= 1.5"}, {'_id': False}))
    print(recommended_stocks)
    ###################################################################랜덤추출
    random_stocks=
    # 2. 성공하면 success 메시지와 함께 stars_list 목록을 클라이언트에 전달합니다.
    return jsonify({'result': 'success', 'msg': 'random_stocks'})


#######고객이 찾은 검색어를 list파일에서 찾아 해당 기업의 주식 정보를 가져오기
@app.route('/api/search/<name>', methods=['GET'])
def search_stocks(name):
    found_stocks = list(db.stocks.find({'name': {'$regex': ".*" + name + ".*"}}, {'_id': False}))
    # 4. 성공하면 success 메시지와 함께 정보 목록을 클라이언트에 전달합니다.
    return jsonify({'result': 'success', 'msg': found_stocks})

#######고객이 저장하는 주식 정보 따로 모으기

# @app.route('/api/mystocks', methods=['POST'])
# def save_mystocks():
    # # 1. 유저의 id를 받습니다.
    id_receive = request.form['id_give']
    # # 2. 유저가 저장한 기업의 code를 받습니다.
    stock_receive=request.form['stock_give']
    # # 3. 유저 id에 해당하는 db에 code를 추가합니다.

    # # 4. 성공하면 success 메시지를 반환합니다.


#######마이페이지를 통해 고객이 저장하는 주식 정보 따로 보여주기
# @ app.route('/api/mystocks', methods=['GET'])

# 1. 유저의 id를 받습니다.
    if_receive = request.form['id_give']

# 2. 유저가 저장한 기업의 정보들을 보냅니다.

# 3. 성공하면 success 메시지를 반환합니다.

#######DB에 있는 정보가 하루 이상 지난 거면 init_db 실행
def refresh_stock_info_job():
    init_db.init_db()


def run_every_schedule_functions():
    schedule.every().day.at('09:00').do(refresh_stock_info_job)  # 매일 09:00 마다 job 함수를 실행
    while True:
        schedule.run_pending()


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
    run_every_schedule_functions()
