from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import urllib.request

driver = webdriver.Chrome(ChromeDriverManager().install())

URL = 'https://www.google.com/imghp?hl=ko&tab=wi'
driver.get(url=URL)

driver.implicitly_wait(time_to_wait=10)

elem = driver.find_element(By.CSS_SELECTOR, '#APjFqb')
elem.send_keys("바다")
elem.send_keys(Keys.ENTER)

elem = driver.find_element(By.TAG_NAME, 'body')
for i in range(60):
    elem.send_keys(Keys.PAGE_DOWN)
    time.sleep(0.1)


try:
    driver.find_element(By.CSS_SELECTOR, '#islmp > div > div > div > div > div.gBPM8 > div.qvfT1 > div.YstHxe > input').click()

    for i in range(60):
        elem.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.1)

except:
    pass

links = []

images = driver.find_elements(By.CSS_SELECTOR, '#islrg > div.islrc > div > div > a.wXeWr.islib.nfEiy > div.bRMDJf.islir > img')

for image in images:
    if image.get_attribute('src') is not None:
        links.append(image.get_attribute('src'))

print ('찾은 이미지 개수 : ', len(links))

for k, i in enumerate(links):
    url = i
    urllib.request.urlretrieve(url, '/Users/user/Desktop/vscode 프로젝트/VSCODE 파이썬/구글 이미지 크롤링/' + str(k) + ".jpg")
    #경로 끝에 / 안붙이면 경로로 지정한 폴더 안으로 안들어감. 폴더 명이 아니라 파일명으로 인식해서 이미지 이름이 1.jpg 가 아니라 구글 이미지 크롤링1.jpg 로 된다.

print('다운로드 완료했습니다')
