from selenium import webdriver
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
import time

options = webdriver.ChromeOptions()
# options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
options.add_argument('lang=ko_KR')
options.add_argument('disable_gpu')
driver = webdriver.Chrome('./chromedriver', options=options)
#{'titles': titles, 'laws': laws, 'dates': dates}

law_xpath = '//*[@id="areaDetail"]/div[2]'
#//*[@id="areaDetail"]/div[2]/div

titles = []
laws = []
dates = []
url = 'https://glaw.scourt.go.kr/wsjo/panre/sjo050.do#'
# driver.get('https://glaw.scourt.go.kr/wsjo/panre/sjo100.do?contId=3205931&q=%EB%8C%80%EB%B2%95%EC%9B%90&nq=&w=panre&section=panre_tot&subw=&subsection=&subId=1&csq=&groups=6,7,5,9&category=&outmax=1&msort=&onlycount=&sp=&d1=&d2=&d3=&d4=&d5=&pg=1&p1=&p2=&p3=&p4=&p5=&p6=&p7=&p8=&p9=&p10=&p11=&p12=&sysCd=WSJO&tabGbnCd=&saNo=&joNo=&lawNm=&hanjaYn=N&userSrchHistNo=&poption=&srch=&range=&daewbyn=N&smpryn=N&idgJyul=01&newsimyn=Y&trtyNm=&tabId=&save=Y&bubNm=')
# time.sleep(1)
# content = driver.find_element_by_xpath('//*[@id="areaDetail"]/div[2]').text
# print(content)
# exit()
driver.get(url)
search_box = driver.find_element_by_name("srchw")  # 검색어 위치 연결
search_box.send_keys("대법원")  # 검색어 보내기
driver.find_element_by_xpath('//*[@id="search"]/div[2]/fieldset/a[1]').click()  # 검색버튼
time.sleep(0.2)
driver.find_element_by_xpath('//*[@id="search"]/div[2]/fieldset/div/p/a').click()  # 자동완성 창 닫기
time.sleep(0.5)
#driver.find_element_by_xpath('//*[@id="groupList"]/li[5]/ul/li[1]/a').click()
#time.sleep(0.5)
#driver.find_element_by_xpath('//*[@id="tabwrap"]/div/div/div[1]/div[3]/fieldset/ul/li[2]/a/span[1]').click()


next_button_xpath = '//*[@id="tabwrap"]/div/div/div[1]/div[3]/div/fieldset/p/a[1]'  #herf , get-atttribute
next_button_xpath_2 = '//*[@id="tabwrap"]/div/div/div[1]/div[3]/div/fieldset/p/a[2]'
next_button_xpath_3 = '//*[@id="tabwrap"]/div/div/div[1]/div[3]/div/fieldset/p/a[3]'

try:
    for j in range(1,2567): #  2568페이지
        try:
            driver.find_element_by_xpath(next_button_xpath_3).click()
        except:
            driver.find_element_by_xpath(next_button_xpath_2).click()
            try:
                driver.find_element_by_xpath(next_button_xpath).click()
            except:
                print('error0')

        for i in range(0, 20): # 0번ㅇ부터 19번까지 총 20개
            time.sleep(0.5)
            title_xpath = '//*[@id="ln{}"]/td[2]/dl/dt/a[1]/strong/strong'.format(i)
            title = driver.find_element_by_xpath(title_xpath).text
            driver.find_element_by_xpath(title_xpath).click()
            # 페이지에서 클릭을 하면 새 탭이 열리기 때문에 새로 열린 탭을 선택해줘야 한다.
            Window_handles = driver.window_handles
            # 기존의 윈도우탭과 새로운 윈도우탭의 주소가 다르기때문에 window_handels로 그 값을 가져오면
            # ['CDwindow-9800FCC9D9BA8DB21936C9EADCE05B78', 'CDwindow-E5552046DFEEA9ED5F2E4BE91910B2DA'] 0번이 기존 윈도우탭 1번이 새로열린 윈도우탭
            # 이러한 리스트에 들어가기 때문에 1번 인덱스를 줘서 새로운 창으로 이동한다.
            driver.switch_to.window(Window_handles[1])
            try:
                time.sleep(1)
                law = driver.find_element_by_xpath(law_xpath).text
                driver.close()
                # 새로운 창에서 텍스트값을 가져온 다음 close를 통해 창을 닫아주고 (현재 선택된 창만 닫힙니다)
                driver.switch_to.window(Window_handles[0])
                # 같은방법으로 기존 윈도우탭으로 돌아가야 합니다.
            except:
                print('except01')
                continue
            titles.append(title)
            laws.append(law)

except:
    print('error')
