# 텍스트 마이닝 (Text Mining)

1. 정보 검색 (HDFS)
- 우리는 스크랩핑(Scraping) 기법 이용하여 지니뮤직(Genie) 으로부터 100개 앨범의 장르 및 수록곡 가사 비정형 문서 데이터를 자동화로 얻어내었음.
- 다만 앨범 100개로는 데이터 부족할 수 있으니 추가 스크랩핑 필요성

1. 자연어 처리 (Kafka, Spark)
- 1차 제거
    - HTML 태그, \n 등 태그 삭제
    - 문장 분리 후 문장부호 추가해 다시 가사 통합
    - 한글 : 맞춤법 및 띄어쓰기 교정 (Py-Hanspell 라이브러리)
    - 영문 : Lowercasting(대문자 → 소문자로 통일)
    - 특수문자 및 문장부호 제거
    
    주의! 한글 맞춤법 교정 우선 하고 문장부호 제거할 것.
    
- 토큰화
    - KoNLPy vs. SOYNLP 비교 후 사용
        
        (1차 제거 완료한 임의 테스트 데이터로 성능 직접 확인해보기. 인터넷에 비교한 글들은 맞춤법 띄어쓰기가 제대로 되지 않은 문장에 대해 실험한 결과 뿐이라 우리가 원하는 상황이 아니므로 동일한 상황이라 판단할 수 없음.)
        
- 2차 제거 : 불용어 제거
    - 기존 불용어 리스트 + 추가한 불용어 리스트 사용하여 제거
    
1. 특징 추출 (MapReduce)
    - 맵리듀스
        - 문서마다 어떤 어간(단어)가 몇 개가 등장하는지 확인
    
    - sparse matrix 생성
        - 원 핫 인코딩을 대신해 맵리듀스 결과로 sparse matrix 생성
        - 이렇게 생성된 matrix 들로 인공지능 모델에 입각해 장르 예측 training 할 것임

1. 문서 분류 (Spark, Zeppelin)
    - 장르 예측
        - sparse matrix 와 장르로 머신러닝 학습 (fit)
        - sparse matrix 로 장르 예측 (predict)

- 예측률 확인
    - accuracy_score() 사용해서 정답률 확인
    - 영향 줄 수 있는 요소들 고쳐서 다시 테스트

1. 군집화

1. 기타 Pyhon 용법
    - 토큰화 : KoNLPy 사용하면 품사 태깅 및 형태소 추출과 같이 단어를 토큰화 할 수 있음
        
        → 장점 : 품사 태깅 시 예를 들면 ‘못’은 부정적인 뜻의 부사도 있지만 망치로 고정하는 물건의 명사도 있는데 이를 구분 가능하게 함. 또한 형태소 추출 시 ‘하는’과 ‘했다’ 모두 똑같은 ‘하다’로 인식하게 함.
        
    
    - 정제 : 불필요한 단어 제거(불용어 제거) : (1) 등장 빈도 너무 적은 단어는 자연어 처리에 도움이 되지 않을 뿐더러 오히려 차원의 저주 문제가 생길 수 있음. 그러므로 감소시키는 게 도움됨. (2) 영어의 경우 길이가 짧은 단어(2, 3)는 주로 삭제함 (3) 정규 표현식 제거 예를 들면 html 태그
        
        +) 필요하다면 직접 불용어 사전 만들 것.
        
    
    - 어간 추출 : 단어의 개수를 줄일 수 있는 기법임. 형태소 추출과 비슷함
    
    - 정수 인코딩 : 단어 등장 빈도수를 바탕으로 sparse matrix 생성하기. (1) 원핫 인코딩
    
2. 필요할 수도 있는 기타 한국어 전처리 패키지
    - PyKoSpacing
        
        띄어쓰기가 되지 않은 문장을 띄어쓰기 한 문장으로 변환해주는 패키지. 띄어쓰기 올바르지 않은 문장을 대비해 전처리 시 사용하자.
        
    - Py-Hanspell
        
        네이버 한글 맞춤법 검사기 바탕으로 만들어진 패키지. 씌어쓰기를 포함해 맞춤법을 보정헤줌.
        
    - SOYNLP
        
        품사 태킹, 단어 토큰화 등 지원하는 단어 토크나이저 패키지. 비지도 학습 이용하며, 신조어 분석이 가능함. 최신 노래들은 신조어 이용해 가사 내는 경우도 있으므로 기존 토크나이저보단 SOYNLP 이용하는 것이 유리. BUT 학습 기반의 토크나이저이므로 학습 과정이 필요해 오버헤드 필수적임.
        
    - [KoSpacing](https://github.com/haven-jeon/PyKoSpacing)
        
        pip install git+https://github.com/haven-jeon/PyKoSpacing.git
        
        띄어쓰기 패키지
        
    - **kss**
        
        문장 분리 패키지. 가사 특성상 문장이 끝나도 마침표가 없는 등 문장부호가 제대로 있지 않을 것이므로 해당 패키지 사용할 것
        
    - https://github.com/ssut/py-hanspell
    네이버 맞추법 감사기 기반 파이썬 맞춤법 검사 패키지.

출처

[https://wikidocs.net/book/2155](https://wikidocs.net/book/2155)

[https://wikidocs.net/92961](https://wikidocs.net/92961)

[https://ebbnflow.tistory.com/246](https://ebbnflow.tistory.com/246)

참고

텍스트 마이닝 [https://ebbnflow.tistory.com/246](https://ebbnflow.tistory.com/246)

하둡과 모델링 [https://m.blog.naver.com/horajjan/221845872805](https://m.blog.naver.com/horajjan/221845872805)

sparse matrix 생성 [https://yamalab.tistory.com/109](https://yamalab.tistory.com/109)
