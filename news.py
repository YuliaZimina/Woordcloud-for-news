import base64

import nltk
from matplotlib import pyplot as plt

nltk.download('punkt')
import pika
from wordcloud import WordCloud
import requests

def callback(ch, method, properties, body):
    print(body)
    wc,news=get_wordcloud(body)
    answer=str(wc)+"spl_"+news
    channel_news.basic_publish(exchange='',
                               routing_key='news-queue',
                               body=answer)

def get_news(date):
    print("im getting news")
    url = ('https://newsapi.org/v2/top-headlines?'
           'q=ID&'
           'from=date&'
           'language=en&'
           'sortBy=popularity&'
           'apiKey=75662bbd26fa4008ac539eb785de2d54')
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
    print(tokens)
    return " ".join(tokens)

def get_wordcloud(date):
    text=get_news(date)
    print("генерирую вордклауд", text)
    # Создать объект экземпляра облака слов
    wordcloud = WordCloud().generate(text)
    # Вывести изображение с заданным именем файла изображения.
    wordcloud.to_file('./WordCloud_pic.png')
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()
    with open('./WordCloud_pic.png', "rb") as image2string:
        converted_string = base64.b64encode(image2string.read())
    return converted_string,text
#maintain_rabbit()

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


"""
def callback(ch, method, properties, body):
    print(body)
    channel_2.basic_publish(exchange='',
                            routing_key='first-queue',
                            body='hi controller')


conn_params = pika.ConnectionParameters('main_rabbit', '5672')
print("rab2")

conn = pika.BlockingConnection(conn_params)

channel_1 = conn.channel()
channel_2 = conn.channel()

channel_1.queue_declare(queue='first-queue')
channel_2.queue_declare(queue='second-queue')

channel_1.basic_consume(on_message_callback=callback,
                        queue='first-queue', auto_ack=True)
print()
time.sleep(2)

try:
    channel_1.start_consuming()
    channel_1.queue_delete(queue='first-queue')
    channel_2.queue_delete(queue='second-queue')
    channel_1.close()
    channel_2.close()
except KeyboardInterrupt:
    channel_1.stop_consuming()
    channel_1.queue_delete(queue='first-queue')
    channel_2.queue_delete(queue='second-queue')
    channel_1.close()
    channel_2.close()
except Exception:
    channel_1.stop_consuming()
    channel_1.queue_delete(queue='first-queue')
    channel_2.queue_delete(queue='second-queue')
    channel_1.close()
    channel_2.close()
    traceback.print_exc(file=sys.stdout)

conn.close()
"""