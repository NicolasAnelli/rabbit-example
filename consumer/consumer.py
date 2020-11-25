#!/usr/bin/env python
import pika
import time
from random import randrange
connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()

channel.queue_declare(queue='first')
channel.queue_declare(queue='second')
channel.queue_declare(queue='third')

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    time.sleep(randrange(0, 5))
    print(" [x] Done")
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume('first', callback)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
