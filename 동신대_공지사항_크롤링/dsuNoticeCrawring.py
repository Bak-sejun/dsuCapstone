from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv
from datetime import datetime


# 브라우저 생성
browser = webdriver.Chrome(ChromeDriverManager().install())

# 웹사이트 열기
URL = 'https://www.dsu.ac.kr/kr/index.php?pCode=notice'
browser.get(url=URL)
browser.implicitly_wait(time_to_wait=10) # 로딩 끝날 때 까지 10초정도 기다림

# csv 파일 생성
file = open(r'/Users/user/Desktop/vscode 프로젝트/VSCODE 파이썬/동신대_공지사항_크롤링/notice.csv', 'w', encoding='UTF-8-sig', newline='')
csvWriter = csv.writer(file)
csvWriter.writerow(['등록일', '제목', '링크'])

# 2023년 1월 1일의 공지사항까지 크롤링 한다
stopDate = datetime(2023, 1, 1)

while True:  
    # 공지사항 정보
    notices = browser.find_elements(By.CSS_SELECTOR, '#contents > div.board-wrap > table > tbody > tr')

    for notice in notices:
        
        noticeWriteDate = notice.find_element(By.CSS_SELECTOR, '#contents > div.board-wrap > table > tbody > tr > td.f-date.date > p').text
        noticeName = notice.find_element(By.CSS_SELECTOR, '#contents > div.board-wrap > table > tbody > tr > td.f-tit.subject > p > a > span').text
        noticeLink = notice.find_element(By.CSS_SELECTOR, '#contents > div.board-wrap > table > tbody > tr > td.f-tit.subject > p > a').get_attribute('href')
        csvWriter.writerow([noticeWriteDate, noticeName, noticeLink])
        noticeDate_dt = datetime.strptime(noticeWriteDate, '%Y-%m-%d')

        #크롤링 잘 되는지 터미널에 출력
        print(noticeWriteDate)
        print(noticeName)
        print(noticeLink)

    # 2023-01-01 미만의 공지사항 크롤링했는지 확인
    if noticeDate_dt < stopDate:
        break

    nextPage = browser.find_element(By.CSS_SELECTOR, '.board-wrap > div.board-list-paging > div > a.nextblock')
    # 다음 페이지로 이동
    nextPage.click()
    time.sleep(1) # 페이지 이동 후, 1초 대기


file.close()
print('동신대 공지사항 크롤링 종료')
