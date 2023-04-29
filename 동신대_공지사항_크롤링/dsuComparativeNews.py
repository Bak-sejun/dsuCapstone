from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv
from datetime import datetime

# 동신대 공지사항 비교과소식 크롤링


# 브라우저 생성
browser = webdriver.Chrome(ChromeDriverManager().install())

# 웹사이트 열기
URL = 'https://www.dsu.ac.kr/kr/index.php?pCode=ecoapi'
browser.get(url=URL)
browser.implicitly_wait(time_to_wait=10) # 로딩 끝날 때 까지 10초정도 기다림

# csv 파일 생성
file = open(r'/Users/user/Desktop/vscode 프로젝트/VSCODE 파이썬/동신대_공지사항_크롤링/comparativeNewsNotice.csv', 'w', encoding='CP949', newline='')
csvWriter = csv.writer(file)
csvWriter.writerow(['시작일', '종료일', '제목', '링크'])

# 2023년 1월 1일의 공지사항까지 크롤링 한다
stopDate = datetime(2023, 1, 1)

# 다음으로 넘길 페이지 번호
nextPageNum = 2

while True:  
    # 공지사항 정보
    notices = browser.find_elements(By.CSS_SELECTOR, '#contents > div.board-wrap > div.board-list-li-wrap > table > tbody > tr')

    for notice in notices:
        
        noticeStartDate = notice.find_element(By.CSS_SELECTOR, '#contents > div.board-wrap > div.board-list-li-wrap > table > tbody > tr > td:nth-child(3) > span').text
        noticeEndDate = notice.find_element(By.CSS_SELECTOR, '#contents > div.board-wrap > div.board-list-li-wrap > table > tbody > tr > td:nth-child(4) > span').text

        noticeName = notice.find_element(By.CSS_SELECTOR, '#contents > div.board-wrap > div.board-list-li-wrap > table > tbody > tr > td.f-tit.subject > p > a').text
        noticeLink = notice.find_element(By.CSS_SELECTOR, '#contents > div.board-wrap > div.board-list-li-wrap > table > tbody > tr > td.f-tit.subject > p > a').get_attribute('href')
        
        # CP949 오류 처리
        try:
            noticeName = noticeName.encode('cp949', 'ignore').decode('cp949')
        except:
            noticeName = noticeName.encode('utf-8-sig', 'ignore').decode('utf-8-sig')


        csvWriter.writerow([noticeStartDate, noticeEndDate, noticeName, noticeLink])
        noticeStartDate_dt = datetime.strptime(noticeStartDate, '%Y-%m-%d')


        #크롤링 잘 되는지 터미널에 출력
        print(noticeStartDate)
        print(noticeEndDate)
        print(noticeName)
        print(noticeLink)


    # 2023-01-01 미만의 공지사항 크롤링했는지 확인
    if noticeStartDate_dt < stopDate:
        break
    
    nextPageNum = nextPageNum + 1
    nextpageSelector = "#contents > div.board-wrap > div.board-list-paging > div > a:nth-child(" + str(nextPageNum) + ")"

    nextPage = browser.find_element(By.CSS_SELECTOR, nextpageSelector)
    # 다음 페이지로 이동
    nextPage.click()
    time.sleep(1) # 페이지 이동 후, 1초 대기


file.close()
print('동신대 비교과소식 공지사항 크롤링 종료')
