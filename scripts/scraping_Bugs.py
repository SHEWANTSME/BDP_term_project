from urllib.request import urlopen
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd


#상세정보 df1 - 앨범ID, 앨범명, 앨범 분류, 앨범 장르
album_info = pd.DataFrame({'앨범ID' : [],
                           '앨범명' : [],
                           '분류' : [], 
                           '장르' : []})
# 이때 장르는 1번 장르만 가져오는 것을 가정으로 함


# 앨범 수록곡 정보 df2 - 수록곡명, 수록곡 길이
album_track = pd.DataFrame({'앨범ID' : [],
                           '곡명' : [],
                           '재생시간' : []})



# 앨범 차트 크롤링
url = "https://music.bugs.co.kr/chart/album/day/total"
html = urlopen(url)
bsObject = BeautifulSoup(html, "html.parser")


# 드라이버
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=options, executable_path='chromedriver')

driver.get(url)


# 앨범 리스트 가져오기
search_albums = len(driver.find_elements(By.XPATH, '//div[@class="albumTitle"]/a'))
count_album = 0
count_track = 0
for index1 in range(search_albums):
    album = driver.find_elements(By.XPATH, '//div[@class="albumTitle"]/a')[index1]
    time.sleep(1)
    album.click()
    #   앨범 정보 가져오기
    album_ID = count_album
    album_title = driver.find_element(By.XPATH, '//div[@class="innerContainer"]/h1').text
    album_kind = driver.find_element(By.XPATH, '//table[@class="info"]/tbody/tr[2]/td').text
    album_genre = driver.find_element(By.XPATH, '//table[@class="info"]/tbody/tr[3]/td').text
    #   앨범 정보 df에 저장
    album_info.loc[count_album] = [album_ID, album_title, album_kind, album_genre]
    tracks = len(driver.find_elements(By.XPATH, '//td/a[@class="trackInfo"]'))
    for index2 in range(tracks):
        track = driver.find_elements(By.XPATH, '//td/a[@class="trackInfo"]')[index2]
        time.sleep(1)
        track.click()
        #   수록곡 정보 가져오기
        track_title = driver.find_element(By.XPATH, '//div[@class="innerContainer"]/h1').text
        track_time = driver.find_element(By.XPATH, '//table[@class="info"]/tbody/tr[4]/td').text
        #   수록곡 정보 df에 저장
        album_track.loc[count_track] = [count_album, track_title, track_time]
        count_track+=1
        driver.back()
        time.sleep(1)
    count_album+=1
    driver.back()
    time.sleep(1)


# csv 파일로 저장
album_info['앨범ID'] = album_info['앨범ID'].astype(int)
album_info.to_csv('album_info.csv')

album_track['앨범ID'] = album_track['앨범ID'].astype(int)
album_track.to_csv('album_track.csv')
