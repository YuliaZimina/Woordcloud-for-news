import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def create_database():
    cursor.execute('CREATE DATABASE wordcloud;')
    connection.commit()

def create_table():
    cursor2.execute('''CREATE TABLE IF NOT EXISTS news_statistics (
    Date text primary key, 
    Statistics text);''')
    connection2.commit()

connection = psycopg2.connect(
                              user="postgres",
                              password="2581211c",
                              port="5432")
connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cursor = connection.cursor()
create_database()
connection.close()
"""
connection2 = psycopg2.connect(
                              user="postgres",
                              password="2581211c",
                              host="127.0.0.1",
                              port="5432",
                              database="wordcloud")
connection2.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cursor2 = connection2.cursor()
create_table()
cursor2.close()
connection2.close()
"""