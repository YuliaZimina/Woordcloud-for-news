import pika
import base64

import psycopg2
from datetime import datetime

from flask import Flask, render_template, url_for, request

global channel_main
global channel_news
global cursor
global connection

global news
global date

global exeption_flag
exeption_flag=False


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
        # connection.autocommit = True
    except:
        print("[INFO] Нет соединения с БД")


def insert_date(date, statistics):
    if get_statistics(date):
        print("Данные за дату уже существуют")
        return
    cursor.execute('''INSERT INTO news_statistics VALUES (%s, %s);''', (date, statistics))
    connection.commit()
    print("Данные добавлены в БД")


def get_statistics(data):
    cursor.execute("SELECT statistics FROM news_statistics WHERE date = %s", (data,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return False


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
    global date
    news = body.decode('utf-8')
    news = news.split("spl_")
    if news[0] == " ":
        print("Empty wordcloud")
        date=datetime.date(datetime.now())
        channel_news.stop_consuming()
        conn.close()
        return
    print('got news')
    if not exeption_flag:
        insert_date(date, str(news[1]))
    decode_img(news[0])
    channel_news.stop_consuming()
    conn.close()


def call_news(date):
    print("calling news")
    maintain_rabbit()
    channel_main.basic_publish(exchange='',
                               routing_key='main-queue',
                               body=date)
    channel_news.basic_consume(on_message_callback=callback,
                               queue='news-queue', auto_ack=True)
    channel_news.start_consuming()


def decode_img(converted_string):
    converted_string = converted_string.encode('utf-8')
    decodeit = open('./static/pics/image.png', 'wb')
    decodeit.write(base64.b64decode((converted_string)))
    decodeit.close()


connect_to_db()

app = Flask(__name__, template_folder="app_templates")


@app.route("/application", methods=["POST", "GET"])
def index():
    return render_template('ui.html')


@app.route("/wordcloud", methods=["POST", "GET"])
def images():
    base = url_for('static', filename='images')
    if request.method == 'POST' or request.method == 'GET':
        global date
        global exeption_flag
        date = request.form.get('datetime')
        try:
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            date = datetime.date(datetime.now())
            print("Incorrect data format, should be YYYY-MM-DD")
            exeption_flag=True
        try:
            call_news(date)
        except Exception:
            print("An error occured")
        print("end of call")
    return render_template('result.html', date=date)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False)
