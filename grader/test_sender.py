import pika

QUEUE = 'sandworm-q-in'

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue=QUEUE, durable=True)
message = 'hello world'
properties = pika.BasicProperties(app_id='test_sender',
                                  content_type='text')
channel.basic_publish('', QUEUE, message, properties)
print " [x] Sent 'Hello World!'"
connection.close()
