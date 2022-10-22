#!/usr/bin/env pytho
# -*- coding: utf-8 -*-
import pika
import time
import random
import traceback
import sys

# =================================================================================================

board = []

for i in range(3):
    board.append(['O'] * 3)


def print_board(board):
    for row in board:
        print(' '.join(row))


def random_row(board):
    return random.randint(1, 3)


def random_col(board):
    return random.randint(1, 3)


ship_row = random_row(board)
ship_col = random_col(board)

print(' '.join([str(ship_row), '- ship row number of player 1']))
print(' '.join([str(ship_col), '- ship column number of player 1']))

# =================================================================================================

conn_params = pika.ConnectionParameters('main_rabbit', '5672')
print("rab1")

conn = pika.BlockingConnection(conn_params)

channel_1 = conn.channel()
channel_2 = conn.channel()

channel_1.queue_declare(queue='first-queue')
channel_2.queue_declare(queue='second-queue')


def callback(ch, method, properties, body):
    time.sleep(5)
    guess_row, guess_col = map(int, body.split())
    if guess_row == 10 and guess_col == 10:
        channel_2.stop_consuming()
        return
    print(' '.join(['Player 2 turn:', str(guess_row), 'row', str(guess_col), 'col']))

    if guess_row == ship_row and guess_col == ship_col:
        print('Player 2 won!')
        channel_1.basic_publish(exchange='',
                                routing_key='first-queue',
                                body='10 10')
        channel_2.stop_consuming()
        return
    else:
        if board[guess_row - 1][guess_col - 1] == 'X':
            print('A shot at this point has already been field!')
        else:
            print('Miss')
            board[guess_row - 1][guess_col - 1] = 'X'

    print('Field of player 1:')
    print_board(board)

    time.sleep(5)
    channel_1.basic_publish(exchange='',
                            routing_key='first-queue',
                            body=str(random.randint(1, 3)) + ' ' + str(random.randint(1, 3)))
    time.sleep(5)
    channel_2.basic_consume(on_message_callback=callback,
                            queue='second-queue', auto_ack=True)


channel_1.basic_publish(exchange='',
                        routing_key='first-queue',
                        body=str(random.randint(1, 3)) + ' ' + str(random.randint(1, 3)))

channel_2.basic_consume(on_message_callback=callback,
                        queue='second-queue', auto_ack=True)

try:
    channel_2.start_consuming()
    channel_1.queue_delete(queue='first-queue')
    channel_2.queue_delete(queue='second-queue')
    channel_1.close()
    channel_2.close()
except KeyboardInterrupt:
    channel_2.stop_consuming()
    channel_1.queue_delete(queue='first-queue')
    channel_2.queue_delete(queue='second-queue')
    channel_1.close()
    channel_2.close()
except Exception:
    channel_2.stop_consuming()
    channel_1.queue_delete(queue='first-queue')
    channel_2.queue_delete(queue='second-queue')
    channel_1.close()
    channel_2.close()
    traceback.print_exc(file=sys.stdout)

conn.close()