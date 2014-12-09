#------------------------------------------------------------------------------
# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------

import pika
import logging
import simplejson as json

#------------------------------------------------------------------------------

QUEUE = 'sandworm-q-out'

#------------------------------------------------------------------------------

def on_message(ch, method, properties, body):
    try:
        message = json.loads(body)
        logging.info('Received archive {} from user {}'.format(
                message['archive_path'],
                message['username']))
    except Exception as e:
        logging.error(e)
    ch.basic_ack(delivery_tag = method.delivery_tag)

#------------------------------------------------------------------------------

def consume():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE, durable=True)
    logging.info('Waiting for messages. To exit press CTRL+C')
    channel.basic_consume(on_message, queue=QUEUE)
    channel.start_consuming()

#------------------------------------------------------------------------------
        
if __name__=='__main__':
    logging.getLogger('').handlers = []
    logging.basicConfig(level=getattr(logging, 'INFO', None),
                        format='// %(message)s')
    consume()
