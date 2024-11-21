from selenium import webdriver
from bs4 import BeautifulSoup  # pip install beautifulsoup4
import time
import pandas as pd

wd = webdriver.Chrome()  # Chrome webdriver 객체 생성

resultList = []  # 크롤링한 결과들 모든 매장 정보가 저장될 빈 리스트 선언

for i in range(1, 201):
    wd.get("https://www.coffeebeankorea.com/store/store.asp")
    # wd.get("http://www.naver.com")
    time.sleep(1)

    try:
        wd.execute_script(f"storePop2('{i}')")
        time.sleep(2)
        html = wd.page_source  # 자바스크립트로 나온 화면의 html 소스
        soup = BeautifulSoup(html, "html.parser")
        # print(soup.prettify())

        store_name = soup.select("div.store_txt > h2")  # 리스트 타입으로 반환
        # print(store_name[0].text.strip())  #<h2>도심공항점</h2>
        store_name = store_name[0].text.strip()  # 매장 이름

        store_info = soup.select("table.store_table > tbody > tr > td")
        # print(store_info[2].text.strip())  # 주소
        # print(store_info[3].text.strip())  # 전화번호

        store_address = store_info[2].text.strip()  # 매장 주소
        store_phone = store_info[3].text.strip()  # 매장 전화번호

        resultList.append([store_name]+[store_address]+[store_phone]+[i])
    except:
        print(f"존재하지 않는 매장 번호 : {i}")
        continue

print(f"총 매장 수 : {len(resultList)}")

coffeeBeanDf = pd.DataFrame(resultList, columns=["매장이름","매장주소","전화번호","매장번호"])
coffeeBeanDf.to_csv("커피빈_매장정보.csv", encoding="cp949", index=False)

