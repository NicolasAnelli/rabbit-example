#!/usr/bin/env python
import pika
import time
from random import randrange
connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()

channel.queue_declare(queue='campainha')
def callback(ch, method, properties, body):
    print(" [x] Entregando pizza de [%r]" % body)
    time.sleep(randrange(0, 5))
    ch.basic_ack(delivery_tag = method.delivery_tag)
    print(" [x] Pizza entregue")

channel.basic_qos(prefetch_count=1)
channel.basic_consume('campainha', callback)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
