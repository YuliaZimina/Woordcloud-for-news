import base64

import nltk

nltk.download('punkt')
import pika
from wordcloud import WordCloud
import requests

def callback(ch, method, properties, body):
    print("got a date", body)
    try:
        date = body.decode('utf-8')
        wc,news=get_wordcloud(date)
        wc=wc.decode('utf-8')
        answer=wc+"spl_"+news
        print("publishing wc and news")
    except Exception:
        print("Exeption while generating wc")
        answer=" "+"spl_"+" "
    channel_news.basic_publish(exchange='',
                               routing_key='news-queue',
                               body=answer)

def get_news(date):
    print("getting news from newsapi")
    url = ('https://newsapi.org/v2/everything?'
           'sources=techcrunch&'
           'from=' + date + '&'
                            'to=' + date + '&'
                                           'language=en&'
                                           'sortBy=popularity&'
                                           'apiKey=110fa14ac4a84455a838cfe39ccf16ee')
    r = requests.get(url)
    r = r.json()
    articles = r["articles"]
    final_articles = []
    for a in articles:
        #print(a)
        final_articles.append(a['description'])
    res = [i for i in final_articles if i is not None]
    tokens_tmp = nltk.word_tokenize(" ".join(res))
    tokens=[]
    for t in tokens_tmp:
        if len(t)>3:
            tokens.append(t)
    return " ".join(tokens)

def get_wordcloud(date):
    text=get_news(date)
    print("generating wordcloud", text)
    # Создать объект экземпляра облака слов
    wordcloud = WordCloud().generate(text)
    wordcloud.to_file('./WordCloud_pic.png')
    with open('./WordCloud_pic.png', "rb") as image2string:
        converted_string = base64.b64encode(image2string.read())
    return converted_string,text


# настройка rabbitmq
conn_params = pika.ConnectionParameters('main_rabbit', '5672')
conn = pika.BlockingConnection(conn_params)
channel_main = conn.channel()
channel_news = conn.channel()
channel_main.queue_declare(queue='main-queue')
channel_news.queue_declare(queue='news-queue')
print("[INFO]выполнена настройка rabbitmq для news")

channel_main.basic_consume(on_message_callback=callback,
                           queue='main-queue', auto_ack=True)
channel_main.start_consuming()


