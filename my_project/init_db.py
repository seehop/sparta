import time
from pymongo import MongoClient
import csv
from selenium import webdriver
from bs4 import BeautifulSoup
import re

def init_db():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
    path = "C:/Users/sohee/Desktop/sparta/develop/chromedriver"
    driver = webdriver.Chrome(path, options=options)
    f = open('firm_stock.csv', 'r', encoding='utf-8')
    print("파일 오픈")

    client = MongoClient('localhost', 27017)
    db = client.dbsparta

    #######리스트에 있는 주식 중 조건에 맞는 주식을 찾아 추천해줌
    # 1. 주식 정보를 db에 저장하는 함수
    def insert_data(row):
        code = row[1]
        name = row[2]
        length_to_expand = 6 - len(code)
        six_length_code = '0' * length_to_expand + code
        print("six_length_code", six_length_code)
        url = 'https://m.stock.naver.com/item/main.nhn#/stocks/' + six_length_code + '/total'
        driver.get(url)
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        prc = soup.select_one(
            'div.end_header_topinfo > div.flick-container.major_info_wrp > div > div:nth-child(2) > div > div.stock_wrp > div.price_wrp > strong').text

        ############################### 종목 정보 더보기 클릭하려면?
        # driver.find_element_by_css_selector('div.total_more > a').click()
        # time.sleep(1)
        ############################### 종목 정보 더보기에서 추가 크롤링을 하려면?
        # time = soup.select_one()
        # '#header > div.end_header_topinfo > div.btm_area > span > span.ymd').text
        eper = soup.select_one(
            '#content_body > div.ct_box.total_info._total_quote_summary > ul > li:nth-child(13) > span').text
        eps = soup.select_one(
            '#content_body > div.ct_box.total_info._total_quote_summary > ul > li:nth-child(12) > span').text
        pbr = soup.select_one(
            '#content_body > div.ct_box.total_info._total_quote_summary > ul > li:nth-child(15) > span').text
        driver.find_element_by_css_selector('ul.lnb_lst > li:nth-child(6) > a').click()
        # content_body > div.ct_box.chart.center._chart > div > ul > li:nth-child(4) > a
        time.sleep(1)
        img_src = soup.select_one('#mflick > div > div.flick-ct._tab.tab1 > div > img')['src']

        ############################### 아래 url에서 정보가 크롤링이 안 돼요 ㅠ_ㅠ?
        url2 = 'https://finance.naver.com/item/main.nhn?code=' + six_length_code
        driver.get(url2)
        time.sleep(1)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        iper = soup.select_one('#tab_con1 > div:nth-child(6) > table > tbody > tr.strong > td > em').text

        if (eper != "N/A" and prc != "N/A" and iper != "N/A" and iper != "N/A"):
            doc = {
                'name': name,
                'code': six_length_code,
                'prc': int(re.sub("[^0-9\.]", "", prc)),
                'eper': float(re.sub("[^0-9\.]", "", eper)),
                'eps': int(re.sub("[^0-9\.]", "", eps)),
                'pbr': float(re.sub("[^0-9\.]", "", pbr)),
                'iper': float(re.sub("[^0-9\.]", "", iper)),
                'img_src': img_src}
            db.stocks.insert_one(doc)
        return ''

    # 2. 기존 mystar 콜렉션을 삭제하고, 출처 url들을 가져온 후, 크롤링하여 DB에 저장합니다.
    def insert_all():
        db.stocks.drop()  # mystar 콜렉션을 모두 지워줍니다.
        rdr = csv.reader(f)
        print("시작")
        for row in rdr:
            if row[1] != "code":
                insert_data(row)

    # 4. 실행하기
    insert_all()
    f.close()


if __name__ == '__main__':
    print(float("16.61"))
    init_db()
