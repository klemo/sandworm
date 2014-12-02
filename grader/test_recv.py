import pika

QUEUE = 'sandworm-q-out'

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))

channel = connection.channel()

channel.queue_declare(queue=QUEUE, durable=True)

print ' [*] Waiting for messages. To exit press CTRL+C'

def callback(ch, method, properties, body):
    print " [x] Received %r" % (body,)
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_consume(callback, queue=QUEUE)
channel.start_consuming()
