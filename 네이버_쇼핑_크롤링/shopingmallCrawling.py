from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import csv

#브라우저 생성
browser = webdriver.Chrome(ChromeDriverManager().install())

#웹사이트 열기
URL = 'https://www.naver.com/'
browser.get(url=URL)
browser.implicitly_wait(time_to_wait=10) #로딩이 끝날 때까지 10초정도 기다려줌

#쇼핑 메뉴 클릭
browser.find_element(By.CSS_SELECTOR, '#NM_FAVORITE > div.group_nav > ul.list_nav.type_fix > li:nth-child(5) > a').click()
time.sleep(2)#쇼핑메뉴 클릭 코드를 실행해서 쇼핑창으로 가기 전에 쇼핑몰 검색창 관련 코드가 실행되는 걸 방지

#쇼핑몰 검색창 클릭
shopingmallSearch = browser.find_element(By.CSS_SELECTOR, '#__next > div > div.pcHeader_header__tXOY4 > div > div > div._gnb_header_area_150KE > div > div._gnbLogo_gnb_logo_3eIAf > div > div._gnbSearch_gnb_search_3O1L2 > form > div._gnbSearch_inner_2Zksb > div > input')
shopingmallSearch.click()

# 검색어 입력
shopingmallSearch.send_keys('아이폰')
shopingmallSearch.send_keys(Keys.ENTER)

# 스크롤 전 스크롤 높이 얻기
before_higt = browser.execute_script('return window.scrollY')#현재창의 스크롤바의 y축 위치를 반환

# 무한 스크롤
while True:
    # 맨 아래로 스크롤을 내린다
    browser.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.END)
    # END 키를 사용하면 스크롤을 맨 아래로 이동한다.

    time.sleep(1)
    #스크롤 사이 페이지 로딩 시간

    # 스크롤 후 스크롤바 높이
    after_higt = browser.execute_script('return window.scrollY')

    #반복문 탈출
    if after_higt == before_higt:
        break
    before_higt = after_higt
    # 스크롤이 마지막에 도달하여 더 내려갈 곳이 없으면 after_higt과 before_higt이 같아진다

# csv 파일 생성. 인자에 w는 파일 열기 모드. write(쓰기) 모드
f = open(r'/Users/user/Desktop/vscode 프로젝트/VSCODE 파이썬/네이버_쇼핑_크롤링/data.csv', 'w', encoding='CP949', newline='')
csvWriter = csv.writer(f)

#상품정보 div
items = browser.find_elements(By.CSS_SELECTOR, '#content > div.style_content__xWg5l > div.list_basis > div > div > div > div > div.basicList_info_area__TWvzp')

for item in items:
    name = item.find_element(By.CSS_SELECTOR, '#content > div.style_content__xWg5l > div.list_basis > div > div > div > div > div.basicList_info_area__TWvzp > div.basicList_title__VfX3c').text
    
    #판매중단 상품이라 가격이 표시 안될 때 예외처리
    try:
        price = item.find_element(By.CSS_SELECTOR, '#content > div.style_content__xWg5l > div.list_basis > div > div > div > div > div.basicList_info_area__TWvzp > div.basicList_price_area__K7DDT > strong > span > span > span.price_num__S2p_v').text
    except:
        price = '판매중단'
        #오류가 나는 부분을 except로 처리

    link = item.find_element(By.CSS_SELECTOR, '#content > div.style_content__xWg5l > div.list_basis > div > div > div > div > div.basicList_info_area__TWvzp > div.basicList_title__VfX3c > a').get_attribute('href')
    #css selector 복붙할때 div 옆에 nth-child 부분 안지우면 nth-child 설정된 부분만 긁어옴
    print(name, price, link)
    #csv 데이터 쓰기
    csvWriter.writerow([name, price, link])

#파일 닫기
f.close()

print('쇼핑몰 크롤링 종료')



