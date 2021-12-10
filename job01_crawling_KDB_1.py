import time

import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import *

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument(
    'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36')
options.add_argument('lang=ko_KR')
options.add_argument('--no-sandbox')  # 가상 환경에서 실행하기 위한 코드
options.add_argument('--disable-dev-shm-usage')
options.add_argument('disable-gpu')

driver = webdriver.Chrome('./chromedriver.exe', options=options)

# //*[@id="viewHeightDiv"]/table/tbody/tr[1]/td[2]/a/text()
# //*[@id="viewHeightDiv"]/table/tbody/tr[3]/td[2]/a/text()
# //*[@id="viewHeightDiv"]/table/tbody/tr[5]/td[2]/a/text()
# //*[@id="viewHeightDiv"]/table/tbody/tr[99]/td[2]/a
# //*[@id="viewHeightDiv"]/table/tbody/tr[299]/td[2]/a/text()           판례 제목
# //*[@id="WideListDIV"]/div/div[6]/ol/li[1]                            페이지 번호
# //*[@id="WideListDIV"]/div/div[6]/ol/li[2]
# //*[@id="WideListDIV"]/div/div[6]/ol/li[5]
# //*[@id="WideListDIV"]/div/div[6]/a[3]/img   //*[@id="listDiv"]/div[2]/a[1]                         다음 페이지
# //*[@id="licPrec218191"]/a/span[1] 왼쪽리스트 판례 제목
# //*[@id="licPrec218187"]/a/span[1]
# //*[@id="licPrec218195"]/a/span[1]
# /html/body/div[4]/div[1]/div[1]/div/div[1]/ul/li[1]
# /html/body/div[4]/div[1]/div[1]/div/div[1]/ul/li[2]
# /html/body/div[4]/div[1]/div[1]/div/div[1]/ul/li[50]
# /html/body/div[4]/div[1]/div[1]/div/div[1]/ul/li[1]/a/span[1]
# /html/body/div[4]/div[1]/div[1]/div/div[1]/ul/li[2]/a/span[1]


url = 'https://law.go.kr/precSc.do?menuId=7&subMenuId=47&tabMenuId=213&query'
driver.get(url)
time.sleep(1)
driver.find_element_by_xpath('//*[@id="viewHeightDiv"]/table/tbody/tr[1]/td[2]/a').click()  # 판례 1 누르기
# time.sleep(5)


def crawling_data():
    law = driver.find_element_by_xpath('//*[@id="bodyContent"]').text
    title = driver.find_element_by_xpath('/html/body/div[4]/div[1]/div[1]/div/div[1]/ul/li[{}]/a/span[1]'.format(j)).text
    date = driver.find_element_by_xpath('//*[@id="contentBody"]/div[1]').text
    date = date.split(",")
    try:
        date = date[0].split()[1:]
        date = "".join(date)
        date = date.rstrip(".")
        dates.append(date)
    except:
        print('date error')
    laws.append(law)
    titles.append(title)


for i in range(1, 26):  # 총 페이지수 1654
    titles = []
    laws = []
    dates = []
    if i % 5 == 0:  # 페이지 수 한 화면에 1~5 페이지 / 5페이지째가되면
        driver.find_element_by_xpath('//*[@id="listDiv"]/div[2]/ol/li[5]/a'.format(i)).click()  # 페이지 숫자 버튼
        time.sleep(1)
        for j in range(1, 51):
            print('{}-{}'.format(i, j), end=" / ")
            if j % 10 == 0:
                print()
            try:
                try:
                    driver.find_element_by_xpath(
                        '/html/body/div[4]/div[1]/div[1]/div/div[1]/ul/li[{}]'.format(j)).click()  # 판례
                except NoSuchElementException:
                    time.sleep(1)
                    driver.find_element_by_xpath(
                        '/html/body/div[4]/div[1]/div[1]/div/div[1]/ul/li[{}]'.format(j)).click()  # 판례
                time.sleep(1)
                crawling_data()
            except:
                time.sleep(1)
                driver.find_element_by_xpath(
                    '/html/body/div[4]/div[1]/div[1]/div/div[1]/ul/li[{}]'.format(j)).click()  # 판례
                time.sleep(1)
                crawling_data()
        if i != 5:
            driver.find_element_by_xpath('//*[@id="listDiv"]/div[2]/a[3]').click()  # 다음 페이지 버튼
            df_law_50 = pd.DataFrame({'titles': titles, 'laws': laws, 'dates': dates})
            print("titles : ", titles)
            print("{}번째 페이지 저장중".format(i), end=" / ")
            df_law_50.to_csv('./crawling_data/law_{}.csv'.format(i), index=False)
            print("{}번째 페이지 저장 완료".format(i))
        elif i == 5:
            driver.find_element_by_xpath('//*[@id="listDiv"]/div[2]/a[1]').click()  # 다음 페이지 버튼
            df_law_50 = pd.DataFrame({'titles': titles, 'laws': laws, 'dates': dates})
            print("titles : ", titles)
            print("{}번째 페이지 저장중".format(i), end=" / ")
            df_law_50.to_csv('./crawling_data/law_{}.csv'.format(i), index=False)
            print("{}번째 페이지 저장 완료".format(i))
    elif i % 5:  # 페이지 1~4는
        if i % 5 != 1:
            driver.find_element_by_xpath('//*[@id="listDiv"]/div[2]/ol/li[{}]/a'.format(i % 5)).click()  # 페이지 숫자 버튼
            time.sleep(1)
        # if (i // 5 > 0) and (i % 5 == 1):
        #     for _ in range(i // 5):
        #         driver.find_element_by_xpath('//*[@id="listDiv"]/div[2]/ol/li[5]/a').click()  # 페이지 숫자 버튼
        #         time.sleep(1)
        #         driver.find_element_by_xpath('//*[@id="listDiv"]/div[2]/a[1]').click()  # 다음 페이지 버튼
        #         time.sleep(1)
        for j in range(1, 51):
            print('{}-{}'.format(i, j), end=" / ")
            if j % 10 == 0:
                print()
            try:
                try:
                    driver.find_element_by_xpath(
                        '/html/body/div[4]/div[1]/div[1]/div/div[1]/ul/li[{}]/a'.format(j)).click()  # 판례
                    time.sleep(1)
                except NoSuchElementException:
                    print('NoSuchElementException 판례번호')
                    time.sleep(1)
                    driver.find_element_by_xpath(
                        '/html/body/div[4]/div[1]/div[1]/div/div[1]/ul/li[{}]'.format(j)).click()  # 판례
                time.sleep(1)
                crawling_data()
            except:
                time.sleep(1)
                crawling_data()
        df_law_50 = pd.DataFrame({'titles': titles, 'laws': laws, 'dates': dates})
        print("titles : ", titles)
        print("{}번째 페이지 저장중".format(i), end=" / ")
        df_law_50.to_csv('./crawling_data/law_{}.csv'.format(i), index=False)
        print("{}번째 페이지 저장 완료".format(i))
driver.close()
