from urllib.request import urlopen
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd


#상세정보 df1 - 앨범ID, 앨범명, 앨범 장르
album_info = pd.DataFrame({'앨범ID' : [],
                           '앨범명' : [],
                           '장르' : []})



# 앨범 차트 크롤링
url = "https://www.genie.co.kr/chart/top200"
html = urlopen(url)
bsObject = BeautifulSoup(html, "html.parser")


# 드라이버
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=options, executable_path='chromedriver')

driver.get(url)


# 앨범 리스트 가져오기
search_albums = len(driver.find_elements(By.XPATH, '//tr[@class="list"]/td[@class="info"]/a[@class="albumtitle ellipsis"]'))
count_album = 0
for index1 in range(search_albums):
    album = driver.find_elements(By.XPATH, '//tr[@class="list"]/td[@class="info"]/a[@class="albumtitle ellipsis"]')[index1]
    time.sleep(1)
    try:
        album.click()
    except ElementClickInterceptedException:
        continue
    #   앨범 정보 가져오기
    album_ID = count_album
    album_title = driver.find_element(By.XPATH, '//div[@class="info-zone"]/h2[@class="name"]').text
    album_genre = driver.find_elements(By.XPATH, '(//ul[@class="info-data"]/li)[2]/span[@class="value"]')[0].text.split(' ')[0]
    #   앨범 정보 df에 저장
    if not (album_info['앨범명'] == album_title ).any():
        album_info.loc[count_album] = [album_ID, album_title, album_genre]
        count_album+=1
    driver.back()
    time.sleep(1)


# csv 파일로 저장
album_info['앨범ID'] = album_info['앨범ID'].astype(int)
album_info.to_csv('album_info_Genie.csv')



print("파일 저장이 완료되었습니다.")
