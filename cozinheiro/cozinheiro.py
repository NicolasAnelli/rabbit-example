#!/usr/bin/env python
import pika
import time
from random import randrange
connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()

channel.exchange_declare(exchange='pizzaria', exchange_type='direct')

pedidosQ = channel.queue_declare(queue='pedidos')
campainhaQ = channel.queue_declare(queue='campainha')

channel.queue_bind(exchange='pizzaria', routing_key='novo-pedido', queue=pedidosQ.method.queue)
channel.queue_bind(exchange='pizzaria', routing_key='pedido-pronto',queue=campainhaQ.method.queue)

def callback(ch, method, properties, body):
    print(" [x] Preparando pizza de [%r]" % body)
    time.sleep(randrange(0, 5))
    ch.basic_ack(delivery_tag = method.delivery_tag)
    print(" [x] Pizza finalizada")
    channel.basic_publish(exchange='pizzaria',
                      routing_key='pedido-pronto',
                      body=body)

channel.basic_qos(prefetch_count=1)
channel.basic_consume('pedidos', callback)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
