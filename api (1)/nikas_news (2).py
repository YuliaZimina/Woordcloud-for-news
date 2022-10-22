import base64
from ctypes import string_at
import requests
import json
import esanpy
from pathlib import Path

from matplotlib import pyplot as plt
from wordcloud import WordCloud
import nltk
nltk.download('punkt')
date = '2022-10-05'
def get_news(date):
    url = ('https://newsapi.org/v2/top-headlines?'
       'q=ID&' 
       'from=date&'
        'to=date'
       'language=en&'
       'sortBy=popularity&'
       'apiKey=75662bbd26fa4008ac539eb785de2d54')
    r = requests.get(url)
    print(r.json())
    r=r.json()
    articles=r["articles"]
    final_articles=[]
    for a in articles:
        print(a)
        if a['description']!="":
            final_articles.append(a['description'])
    #print(final_articles)
    #print ("".join(final_articles))
    #esanpy.start_server()
    #tokens = esanpy.analyzer("".join(final_articles))
    #print (tokens)
    #esanpy.stop_server()
    print(final_articles)
    res = [i for i in final_articles if i is not None]
    tokens_tmp = nltk.word_tokenize(" ".join(res))
    tokens = []
    for t in tokens_tmp:
        if len(t) > 3:
            tokens.append(t)
    print(tokens)
    return tokens
def get_wordcloud(tokens):
    # Читать текстовое содержимое
    current_directory = Path.cwd()
    #text = Path.open(current_directory/"file.txt").read() #нужно вставить название текстового файла для чтения на аглийском
    text = " ".join(tokens)
    print(text)
    # Создать объект экземпляра облака слов
    wordcloud = WordCloud()

    # Загрузить текстовое содержимое в объект облака слов.
    wordcloud.generate(text)
    print(wordcloud)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()
    # Вывести изображение с заданным именем файла изображения.
    wordcloud.to_file('./WordCloud_pic.png')
    with open('./WordCloud_pic.png', "rb") as image2string:
        converted_string = base64.b64encode(image2string.read())
    print(converted_string)

get_wordcloud(tokens=get_news(date))