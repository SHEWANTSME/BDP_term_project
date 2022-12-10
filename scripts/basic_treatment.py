import pandas as pd
import re
import kss
import pykospacing
from hanspell import spell_checker

genre_df = pd.read_csv("album_track_Bugs.csv")

# \n 태그 삭제
def delete_tags(texts):
    corpus = []
    for i in range(len(texts)):
        lyrics = str(texts[i]).split('\n')
        lyrics = list(filter(len, lyrics))
        corpus.append(lyrics)
    return corpus
  
  # 문장 분리 후 부호(.) 추가, 특수문자(괄호) 제거해 다시 가사 통합
def mark_sentences(texts):
    corpus = []
    for i in range(len(texts)):
        for j in range(len(texts[i])):
#             texts[i][j] = add_marks(texts[i][j])
            texts[i][j] = re.sub("\(|\)|\n", "",  texts[i][j])
        corpus.append(texts[i])
    return corpus

# 문장에 부호 추가
def add_marks(text):
    new_text = [text]
    new_text.append(".")
    new_text = ''.join(new_text)
    return new_text

# 띄어쓰기 교정
def space(texts):
    spacing = pykospacing.Spacing()
    corpus = []
    for i in range(len(texts)):
        for j in range(len(texts[i])):
            texts[i][j] = spacing(texts[i][j])
        corpus.append(texts[i])
    return corpus

# 맞춤법 교정 (띄어쓰기 포함)
def grammer(texts):
    corpus = []
    for i in range(len(texts)):
        for j in range(len(texts[i])):
            try:
                texts[i][j] = spell_checker.check(texts[i][j]).checked
            except:
                continue
        corpus.append(texts[i])
    return corpus

# 대문자 -> 소문자
def toLowercase(texts):
    corpus = []
    for i in range(len(texts)):
        for j in range(len(texts[i])):
            temp = texts[i][j]
            texts[i][j] = temp.lower()
        corpus.append(texts[i])
    return corpus


genre_df['가사'] = delete_tags(genre_df['가사'])
genre_df['가사'] = mark_sentences(genre_df['가사'])  
genre_df['가사'] = delete_tags(genre_df['가사'])
genre_df['가사'] = mark_sentences(genre_df['가사'])
# 맞춤법 교정 작업 오래 걸리므로 나눠 작업하기 (혹시 중간에 에러 나면 다시 해야 하니까)
genre_df['가사'] = grammer(genre_df['가사'])
genre_df['가사'] = toLowercase(genre_df['가사'])


# csv 파일로 저장
genre_df.to_csv('lyrics_basic_Bugs.csv', index=False)
