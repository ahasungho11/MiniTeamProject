from bs4 import BeautifulSoup
from selenium import webdriver
import time
import datetime as dt
from dateutil.relativedelta import relativedelta
from selenium.webdriver.common.by import By
from konlpy.tag import Okt
from wordcloud import WordCloud
from collections import Counter
import matplotlib.pyplot as plt
import platform
import pandas as pd


def openUrl(driver):
    # 로그인 정보
    login_url = 'https://nid.naver.com/nidlogin.login'
    naver_id = "qweriii1977"
    naver_pw = "fkfk2rj2@!##H"

    # 드라이버 실행 후 로그인
    driver.get(login_url)
    driver.implicitly_wait(2)

    # execute_script 함수 사용하여 자바스크립트로 id,pw 넘겨주기
    driver.execute_script("document.getElementsByName('id')[0].value=\'" + naver_id + "\'")
    driver.execute_script("document.getElementsByName('pw')[0].value=\'" + naver_pw + "\'")

    # 로그인 버튼 클릭하기
    driver.find_element(By.XPATH, '//*[@id="log.login"]').click()
    time.sleep(1)

    # 기기등록 버튼 클릭하기
    driver.find_element(By.XPATH, '//*[@id="new.save"]').click()
    time.sleep(1)

def createList(driver, item_title, item_date):
    now = dt.datetime.now()
    date = now

    while True:
        count = 1

        while True:
            # 크롤링 진행하려는 카페 주소(중고나라)
            cafe_url = '''
            https://cafe.naver.com/joonggonara?iframe_url=/ArticleSearchList.nhn%3Fsearch.clubid=10050146%26search.
            menuid=440%26search.media=0%26search.searchdate={0}{1}%26search.defaultValue=1%26userDisplay=15%26search.
            onSale=1%26search.option=3%26search.sortBy=date%26search.searchBy=0%26search.searchBlockYn=0%26search.
            query=kg%26search.viewtype=title%26search.page={2}
            '''.format(dt.datetime.strftime(date - dt.timedelta(days=6), '%Y-%m-%d'), dt.datetime.strftime(date, '%Y-%m-%d'), count)

            driver.get(cafe_url)

            # iframe으로 접근
            driver.switch_to.frame('cafe_main')
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # 네이버 카페 구조 확인후 게시글 내용만 가저오기
            datas = soup.find_all(class_='td_article')
            dates = soup.find_all(class_='td_date')

            if datas == []:
                break

            for data in datas:
                article_title = data.find(class_='article')
                article_title = article_title.get_text().strip()
                item_title.append(article_title)

            for day in dates: item_date.append(day.text)

            count += 1

        date = date - dt.timedelta(weeks=1)
        if date < (now - relativedelta(years=2)): break


def createCSV(item_title, item_date):
    data = {'Title': item_title, 'Date': item_date}
    df = pd.DataFrame(data)
    df.drop_duplicates(['Title'], ignore_index=True, inplace=True)
    df.to_csv('item_list.csv', encoding='utf-8-sig')


# def wordcloud():

def main():
    item_title = []
    item_date = []

    driver = webdriver.Chrome('C:\workspace\chromedriver')

    openUrl(driver)
    createList(driver, item_title, item_date)
    createCSV(item_title, item_date)


main()