import pika

QUEUE = 'sandworm-q-in'

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue=QUEUE)
channel.basic_publish(exchange='', routing_key=QUEUE, body='Hello World!')
print " [x] Sent 'Hello World!'"
connection.close()
