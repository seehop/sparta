import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import csv

f = open('firm_stock.csv', 'r', encoding='utf-8')
print("파일 오픈")

client = MongoClient('localhost', 27017)
db = client.dbsparta

#######리스트에 있는 주식 중 조건에 맞는 주식을 찾아 추천해줌

#1. 주식 정보를 db에 저장하는 함수
def insert_data(code):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get('https://m.stock.naver.com/item/main.nhn#/stocks/' + code, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    prc = soup.select('# header > div.end_header_topinfo > div.flick-container.major_info_wrp > div > div:nth-child(2) > div > div.stock_wrp > div.price_wrp >')['strong.data_current_price']

    uls = soup.select('# content_body > div.ct_box.total_info._total_quote_summary.ti_on > ul')
    for ul in uls:
        per = ul.select_one('li:nth-child(11) > span').text
        eps = ul.select_one('li:nth-child(12) > span').text

    doc={
        'per': per,
        'eps': eps
    #클릭해야 나오는 이미지 정보 스크래핑은 어떻게 하지?
    }

    db.stocks.insert_one(doc)
    print('db 저장 완료!', name)

    return urls

#2. 기존 mystar 콜렉션을 삭제하고, 출처 url들을 가져온 후, 크롤링하여 DB에 저장합니다.
def insert_all():
    db.stocks.drop()  # mystar 콜렉션을 모두 지워줍니다.
    rdr = csv.reader(f)
    print("시작")
    for dbcode in rdr:
        insert_data(dbcode[1])


#4. 실행하기
insert_all()
f.close()
