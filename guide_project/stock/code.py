import schedule

from selenium import webdriver
from bs4 import BeautifulSoup

import time

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_mail(stock_name):
    # 내 이메일 정보를 입력합니다.
		me = "test1@abc.com"
		# 내 비밀번호를 입력합니다.
		my_password = "wpfzfpqiubxjnjun"
		# 이메일 받을 상대방의 주소를 입력합니다.
		you = "test2@abc.com"

    ## 여기서부터 코드를 작성하세요.
    # 이메일 작성 form을 받아옵니다.
    msg = MIMEMultipart('alternative')
    # 제목을 입력합니다.
    msg['Subject'] = "알림!"
    # 송신자를 입력합니다.
    msg['From'] = me
    # 수신자를 입력합니다.
    msg['To'] = you

    # 이메일 내용을 작성합니다.
    html = stock_name+' 주식을 한번 보세요!'
    # 이메일 내용의 타입을 지정합니다.
    part2 = MIMEText(html, 'html')
    # 이메일 form에 작성 내용을 입력합니다
    msg.attach(part2)
    ## 여기에서 코드 작성이 끝납니다.

    # Gmail을 통해 전달할 것임을 표시합니다.
    s = smtplib.SMTP_SSL('smtp.gmail.com')
    # 계정 정보를 이용해 로그인합니다.
    s.login(me, my_password)
    # 이메일을 발송합니다.
    s.sendmail(me, you, msg.as_string())
    # 이메일 보내기 프로그램을 종료합니다.
    s.quit()

def get_my_stock():
    ### option 적용 ###
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")

    driver = webdriver.Chrome('chromedriver', options=options)
    ##################

    codes = ['005930', '035420', '017670', '096770', '035720']

    for code in codes:
        # 네이버 주식페이지 url을 입력합니다.
        url = 'https://m.stock.naver.com/item/main.nhn#/stocks/' + code + '/total'

        # 크롬을 통해 네이버 주식페이지에 접속합니다.
        driver.get(url)

        # 정보를 받아오기까지 2초를 잠시 기다립니다.
        time.sleep(2)

        # 크롬에서 HTML 정보를 가져오고 BeautifulSoup을 통해 검색하기 쉽도록 가공합니다.
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        name = soup.select_one(
            '#header > div.end_header_topinfo > div.flick-container.major_info_wrp > div > div:nth-child(2) > div > div.item_wrp > div > h2').text

        current_price = soup.select_one(
            '#header > div.end_header_topinfo > div.flick-container.major_info_wrp > div > div:nth-child(2) > div > div.stock_wrp > div.price_wrp > strong').text

        rate = soup.select_one('#header > div.end_header_topinfo > div.flick-container.major_info_wrp > div > div:nth-child(2) > div > div.stock_wrp > div.price_wrp > div > span.gap_rate > span.rate').text

        print(name,current_price,rate)

        if (float(rate) > 4):
            print('send',name)
            send_mail(name)

    print('-------')
    # 크롬을 종료합니다.
    driver.quit()

def job():
    get_my_stock()

def run():
    schedule.every(10).seconds.do(job) #10초에 한번씩 실행
    while True:
        schedule.run_pending()

if __name__ == "__main__":
    run()