#------------------------------------------------------------------------------
# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------

import time
import pika
import logging
import simplejson as json

#------------------------------------------------------------------------------

QUEUE_CONSUME = 'sandworm-q-out'
QUEUE_PUBLISH = 'sandworm-q-in'

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
    ### simulate work ###
    time.sleep(5)
    message['finished'] = True
    update_progress(ch, message)

#------------------------------------------------------------------------------

def consume():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_CONSUME, durable=True)
    channel.queue_declare(queue=QUEUE_PUBLISH, durable=True)
    logging.info('Waiting for messages. To exit press CTRL+C')
    channel.basic_consume(on_message, queue=QUEUE_CONSUME)
    channel.start_consuming()

#------------------------------------------------------------------------------
    
def update_progress(channel, content):
    properties = pika.BasicProperties(
        app_id='exec-worker',
        content_type='application/json',
        delivery_mode = 2, # make message persistent
        )
    message = json.dumps(content, ensure_ascii=False)
    channel.basic_publish(exchange='', routing_key=QUEUE_PUBLISH,
                          body=message, properties=properties)
        
    logging.info('Sent {}'.format(content))

#------------------------------------------------------------------------------
        
if __name__=='__main__':
    logging.getLogger('').handlers = []
    logging.basicConfig(level=getattr(logging, 'INFO', None),
                        format='// %(message)s')
    consume()
