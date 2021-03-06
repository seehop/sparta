from pymongo import MongoClient
from flask import Flask, render_template, jsonify, request
import csv
from datetime import datetime
import init_db
import random
import schedule
import re

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
    recommended_stocks = list(db.stocks.find({"$where": "this.eper < this.iper && this.pbr <= 1"}, {'_id': False}))
    random.shuffle(recommended_stocks)
    print(recommended_stocks)
    ###################################################################랜덤추출
    random_stocks = recommended_stocks[:3]
    # 2. 성공하면 success 메시지와 함께 stars_list 목록을 클라이언트에 전달합니다.
    return jsonify({'result': 'success', 'stocks': random_stocks})


#######고객이 찾은 검색어를 list파일에서 찾아 해당 기업의 주식 정보를 가져오기
@app.route('/api/search/<name>', methods=['GET'])
def search_stocks(name):
    #found_stocks = list(db.stocks.find({'name': {'$regex': ".*" + name + ".*"}}, {'_id': False}))
    rgx = re.compile('.*' + name + '.*', re.IGNORECASE)  # compile the regex
    found_stocks = list(db.stocks.find({'name': rgx}, {'_id': False}))
    print(name,found_stocks)
    # 4. 성공하면 success 메시지와 함께 정보 목록을 클라이언트에 전달합니다.
    return jsonify({'result': 'success', 'stocks': found_stocks})

## 2번째 HTML 역할을 하는 부분
@app.route('/mystocks/<username>')
def mystocks(username):
    return render_template('mystocks.html', ID=username)

#######고객이 저장하는 주식 정보 따로 모으기
@app.route("/api/mystocks/<username>", methods=["POST"])
def mystocks_post(username):
    code = request.form['code_give']

    found_username_and_stocks = db.saved_stocks.find_one({'username': username}, {'code': code},{'_id': False}) ###########지금 여기서 문제가 생기는 듯
    found_username = db.saved_stocks.find_one({'username':username}, {'_id':False})

    if found_username_and_stocks is None:
        if found_username is None:
            db.saved_stocks.insert_one({'username': username, 'code': code})
            return jsonify({'result': 'success'})
        else:
            new_codes = list(found_username['code'])
            new_codes.append(code)
            db.saved_stocks.update_one(
                {'username': username},
                {'$set': {'code': new_codes}}
            )
            return jsonify({'result': 'success'})
    else:
        return jsonify({'result':'overlap'})



#######고객이 저장한 주식 정보 따로 보여주기
@app.route("/api/mystocks/<username>", methods=["GET"])
def mystocks_get(username):
    # { "username": "lopun", "stock_codes": ["265520", ...] }
    # username_and_stocks 테이블에서 username에 해당하는 값을 찾는다
    found_username = db.saved_stocks.find_one({'username': username}, {'_id': False})
    print(found_username)
    # username에 해당하는 값이 없으면 fail
    if found_username is None:
        return jsonify({"result": "failed"})
    # username에 해당하는 값이 있으면
    else:
        # stock_codes들로
        codes = list(found_username["code"])
        print(codes)
        # 진짜 stocks를 찾는다. 이 때 $in이라는 문법을 사용함
        stocks = list(db.stocks.find({'code': {'$in': codes}}, {'_id': False}))
        # 클라이언트에게 모든 stock들을 내려주고 마무리
        return jsonify({"result": "success", "stocks": stocks})


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
