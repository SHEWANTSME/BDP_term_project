# 멜론 시대별 차트
# album_info_melon =[앨범ID, 앨범명 , 장르] -> melon은 분류 정보가 없다
# album_track_melon =[앨범ID,곡명,가사] -> melon은 재생시간 정보가 없다

from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import requests
import pandas as pd
import re
import math

#상세정보 df1 - 앨범ID, 앨범명,  앨범 장르
album_info = pd.DataFrame({'앨범ID' : [],
                           '앨범명' : [],
                           '분류' : [],
                           '장르' : []})


# 앨범 수록곡 정보 df2 - 앨범ID, 수록곡명, 가사
album_track = pd.DataFrame({'앨범ID' : [],
                           '곡명' : [],
                           '가사' : []})

# melon은 user-agent를 써주지 않으면 406 Not Acceptable로 에러가 난다. 본인이 로봇이 아닌 사람이라고 말 해줘야 한다.
header = {
    'User-Agent' :('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'),
}

# album마다 track의 개수가 다르기때문에 따로 cnt를 해줘야 한다.
global total_album_track_cnt 
total_album_track_cnt=0
# 2000년부터 2021년까지의 데이터를 볼 것이다.
cnt = 2000
# 각각의 순위마다 두번을 눌러줘야함 + 중복되는 앨범이 시대별로 존재할 수 있으니 중복 방지를 위한 dictionary생성
check_dic={'album_name':'kimjunehyun'}

# 멜론 홈페이지의 특성상 0~50위, 51위부터 100위가 버튼 하나로 내용이 바뀌기 때문에
# Run_Track함수로 만들어 인자값만 바꿔서 실행되도록 했다.
def Run_Track(aa,bb):
    global total_album_track_cnt
    for i in range(aa,bb):
        driver.find_elements(By.XPATH, '//div[@class="ellipsis rank03"]/a')[i].click()
        album_kind = driver.find_elements(By.XPATH, '//div[@class="info"]/span[@class="gubun"]')[0].text
        time.sleep(1)
        album_genre = driver.find_elements(By.XPATH, '//div[@class="meta"]/dl[@class="list"]/dd')[1].text
        album_name = driver.find_elements(By.XPATH, '//div[@class="info"]/div[@class="song_name"]')[0].text
        # 이미 크롤링한 앨범이면 continue
        if album_name in check_dic is True:
            continue
        else: check_dic[album_name] = 1
        album_info.loc[i] = [math.trunc(i), album_name, album_kind, album_genre]
        listed_song_size = len(driver.find_elements(By.XPATH, '//tr[@data-group-items="cd1"]'))
        time.sleep(1)
        for j in range(listed_song_size):
            driver.find_elements(By.XPATH, '//td/div[@class="wrap"]/a')[j].click()
            try:
                driver.find_elements(By.XPATH, '//div[@class="wrap_lyric"]/button')[0].click()
                song_lyric = driver.find_elements(By.XPATH, '//div[@class="lyric on"]')[0].text
                time.sleep(1)
            except: # 성인인증이 필요하거나, 가사가 존재하지 않는 경우
                song_lyric = " "
            song_name = driver.find_elements(By.XPATH, '//div[@class="info"]/div[@class="song_name"]')[0].text
            album_track.loc[total_album_track_cnt] = [math.trunc(i),song_name , song_lyric]
            total_album_track_cnt+=1
            driver.back()
            time.sleep(1)
        driver.back()
        time.sleep(1)

# 2021년까지의 시대별 차트가 필요하므로 다음과 같이 코드를 구성했다.
while(cnt<2022):
    url = "https://www.melon.com/chart/age/index.htm?chartType=YE&chartGenre=KPOP&chartDate="
    url = url + str(cnt)
    html= requests.get(url,headers=header).text # requests를 쓸때는 .text를 써줘야 내용을 얻어올 수 있다.
    bsObject = BeautifulSoup(html , "html.parser")
    # 현재 chromewebdriver의 로컬 위치
    path = "C:/Users/qhdms/Downloads/chromedriver_win32/chromedriver.exe"
    driver = webdriver.Chrome(path)
    driver.get(url)   
    Run_Track(0,50)
    driver.find_elements(By.XPATH ,'//div[@class="paginate chart_page"]/span/a' )[0].click()
    Run_Track(50,100)
    cnt+=1


album_info.to_csv('album_info_melon.csv', index=False)
album_track.to_csv('album_track_melon.csv', index=False)

print('DONE!!')