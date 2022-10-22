import pika
import time
import random
import traceback
import sys

import psycopg2

from flask import Flask, render_template, url_for, request

global channel_main
global channel_news
global cursor
global connection

global news

def connect_to_db():
    def create_table():
        cursor.execute('''CREATE TABLE IF NOT EXISTS news_statistics (
        Date text primary key, 
        Statistics text);''')
        connection.commit()
    try:
        global cursor
        global connection
        connection = psycopg2.connect(
            user="postgres",
            password="2581211c",
            database="wordcloud",
            host="db",
            port="5432")
        print("[INFO] Подключение с БД установлено")
        cursor = connection.cursor()
        create_table()
    except:
        print("[INFO] Нет соединения с БД")

def insert_date(date, statistics):
    try:
        cursor.execute('''INSERT INTO news_statistics VALUES (%s, %s);''', (date, statistics))
        connection.commit()
        print("Данные добавлены в БД")
    except:
        print("Данные за дату уже существуют")

def maintain_rabbit():
    global channel_main
    global channel_news
    global conn_params
    global conn

    # настройка rabbitmq
    conn_params = pika.ConnectionParameters('main_rabbit', '5672')
    conn = pika.BlockingConnection(conn_params)
    channel_main = conn.channel()
    channel_news = conn.channel()
    channel_main.queue_declare(queue='main-queue')
    channel_news.queue_declare(queue='news-queue')
    print("[INFO]выполнена настройка rabbitmq для controller")

def callback(ch, method, properties, body):
    global news
    news=body.split(b"spl_")
    #print(wc,'got wordcloud')
    print('got news')
    insert_date(date, str(news[1]))
    #channel_news.stop_consuming()
    #conn.close()
    return news[0],news[1]

def call_news(date):
    print("calling news")
    channel_main.basic_publish(exchange='',
                            routing_key='main-queue',
                            body=date)
    print("called")
    channel_news.basic_consume(on_message_callback=callback,
                            queue='news-queue', auto_ack=True)
    channel_news.start_consuming()

connect_to_db()


app = Flask(__name__, template_folder="app_templates")
@app.route("/application", methods=["POST", "GET"])
def index():
    if request.method == 'POST':
        print(request.form.get('datetime'))
        maintain_rabbit()
        date=request.form.get('datetime')
        call_news(date)
        print("writing in db")
        #insert_date(date, str(news[1]))
        return render_template('ui2.html')
    return render_template('ui.html')
if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=False)

date='2022-10-16'


