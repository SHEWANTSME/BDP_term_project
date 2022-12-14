genres_xpath = {'발라드':'//*[@id="container"]/section/div/ul/li[1]/ul/li[1]/a',
                '댄스/팝':'//*[@id="container"]/section/div/ul/li[1]/ul/li[2]/a',
                '랩/힙합':'//*[@id="container"]/section/div/ul/li[1]/ul/li[5]/a'
               }


    

ID = 0
# 차트 페이지로 in
for i in genres_xpath:
    search = driver.find_element(By.XPATH, genres_xpath[i])
    time.sleep(1)
    try:
        search.click()
    except Exception:
        continue
    time.sleep(1)

    # 차트 내 곡 수 
    songs_num = len(driver.find_elements(By.XPATH, '//*[@id="CHARTday"]/table/tbody/tr/td[4]/a'))
    # 곡 상세페이지로 in

    for index in range(songs_num):
        album = driver.find_elements(By.XPATH, '//*[@id="CHARTday"]/table/tbody/tr/td[4]/a')[index]
        time.sleep(1)
        try:
            album.click()
        except Exception:
            continue
        # 곡 정보 가져오기
        title = driver.find_element(By.XPATH, '//div[@class="innerContainer"]/h1').text
        isin = False
        for i in range(len(driver.find_elements(By.XPATH, '//*[@id="container"]/section[1]/div/div[1]/table/tbody/tr'))):
            if driver.find_elements(By.XPATH, '//*[@id="container"]/section[1]/div/div[1]/table/tbody/tr/th')[i].text == '아티스트':
                artist = driver.find_element(By.XPATH, '//*[@id="container"]/section[1]/div/div[1]/table/tbody/tr[{}]/td/a'.format(i+1)).text
                isin = True
        if not isin:
            artist = None
        genre = i
        try:
            track_lyrics = driver.find_element(By.XPATH, '//div[@class="lyricsContainer"]/xmp').text
        except Exception:
            track_lyrics = None
        # 데이터프레임으로 저장
        music.loc[ID] = [ID, title, artist, genre, track_lyrics]
        ID+=1
        driver.back()
        time.sleep(1)
    driver.back()
    time.sleep(1)

        
        

        
    
    
    

# csv 파일로 저장
music = music.astype({'곡ID':'int', '곡명':'string', '아티스트':'string', '장르':'string', '가사':'string'})
music.to_csv('Music.csv', index=False)




print("파일 저장이 완료되었습니다.")
