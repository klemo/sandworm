import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='sandworm-q0')

channel.basic_publish(exchange='',
                      routing_key='sandworm-q0',
                      body='Hello World!')
print " [x] Sent 'Hello World!'"
connection.close()
