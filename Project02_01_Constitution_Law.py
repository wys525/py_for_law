from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import pandas as pd
import re
import time
import pyautogui


options = webdriver.ChromeOptions()
options.add_argument('lang=ko_KR')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('disable-gpu')
driver = webdriver.Chrome('./chromedriver',
                          options=options)
options.add_argument('--blink-settings=imagesEnabled=false')

##로앤비에서 크롤링 작업 세팅
laws = []
const=[]
for i in range(2,262,2):
    url='https://lawnb.com/Info/ContentView?sid=L0009FCA77B8B2C6#P130' #&sort=desc&pg={l}&pageSize=20&filter_search=False
    driver.get(url)
    # time.sleep(0.5)
    # titles = []


    law = driver.find_element_by_xpath(
        '//*[@id="view_content"]/div[{}]'.format(i)).text
    print(law)
    laws.append(law)


##법조문 조항과 법조문 내용 맞춰줌
for k in range(130):
    print('헌법' +str(k+1) + '조')
    const.append('헌법' +str(k+1) + '조')

##DF로 그리고 CSV로 출력
df_const=pd.DataFrame({'const':const, 'laws':laws})
df_const.to_csv('./Laws/Const.csv', index=False)

