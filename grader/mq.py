#------------------------------------------------------------------------------
# http://pika.readthedocs.org/en/latest/examples/tornado_consumer.html
# http://pika.readthedocs.org/en/latest/examples/asynchronous_publisher_example.html
#------------------------------------------------------------------------------

import pika
import logging
import simplejson as json

#------------------------------------------------------------------------------

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)

#------------------------------------------------------------------------------

class QConsumer(object):
    '''
    Async pika/rabbitmq receiver
    '''

    def __init__(self, queue, url='amqp://guest:guest@localhost:5672/%2F'):
        self.exchange = 'message'
        self.exchange_type = 'topic'
        self.queue = queue
        self.routing_key = self.queue
        self._url = url
        self._connection = None
        self._channel = None
        self._closing = False
        self._consumer_tag = None
        # connect to rabbitmq
        self._connection = self.connect()

    def connect(self):
        LOGGER.info('QConsumer: Connecting to %s', self._url)
        return pika.adapters.TornadoConnection(pika.URLParameters(self._url),
                                               self.on_connection_open)

    def on_connection_open(self, unused_connection):
        LOGGER.info('QConsumer: Connection opened')
        self._connection.add_on_close_callback(self.on_connection_closed)
        self._connection.channel(on_open_callback=self.on_channel_open)

    def on_channel_open(self, channel):
        LOGGER.info('QConsumer: Channel opened')
        self._channel = channel
        self._channel.add_on_close_callback(self.on_channel_closed)
        self._channel.exchange_declare(self.on_exchange_declareok,
                                       self.exchange,
                                       self.exchange_type)

    def on_exchange_declareok(self, unused_frame):
        LOGGER.info('QConsumer: Exchange declared')
        self._channel.queue_declare(self.on_queue_declareok, self.queue)

    def on_queue_declareok(self, method_frame):
        LOGGER.info('QConsumer: Binding %s to %s with %s',
                    self.exchange, self.queue, self.routing_key)
        self._channel.queue_bind(self.on_bindok, self.queue,
                                 self.exchange, self.routing_key)

    def on_connection_closed(self, connection, reply_code, reply_text):
        self._channel = None
        LOGGER.warning(
            'QConsumer: Connection closed, reopening in 5 seconds: (%s) %s',
            reply_code, reply_text)
        self._connection.add_timeout(5, self.reconnect)

    def reconnect(self):
        if not self._closing:
            # Create a new connection
            self._connection = self.connect()

    def close_connection(self):
        LOGGER.info('QConsumer: Closing connection')
        self._connection.close()

    def on_channel_closed(self, channel, reply_code, reply_text):
        LOGGER.warning('QConsumer: Channel %i was closed: (%s) %s',
                       channel, reply_code, reply_text)
        self._connection.close()

    def add_on_cancel_callback(self):
        LOGGER.info('QConsumer: Adding consumer cancellation callback')
        self._channel.add_on_cancel_callback(self.on_consumer_cancelled)

    def on_consumer_cancelled(self, method_frame):
        LOGGER.info(
            'QConsumer: Consumer was cancelled remotely, shutting down: %r',
            method_frame)
        if self._channel:
            self._channel.close()

    def on_message(self, unused_channel, basic_deliver, properties, body):
        LOGGER.info('QConsumer: Received message # %s from %s: %s',
                    basic_deliver.delivery_tag, properties.app_id, body)
        self._channel.basic_ack(basic_deliver.delivery_tag)

    def on_cancelok(self, unused_frame):
        LOGGER.info('QConsumer: RabbitMQ acknowledged the cancellation of the consumer')
        self.close_channel()

    def stop_consuming(self):
        if self._channel:
            LOGGER.info('QConsumer: Sending a Basic.Cancel RPC command to RabbitMQ')
            self._channel.basic_cancel(self.on_cancelok, self._consumer_tag)

    def start_consuming(self):
        LOGGER.info('QConsumer: Start consuming: Issuing consumer related RPC commands')
        self.add_on_cancel_callback()
        self._consumer_tag = self._channel.basic_consume(self.on_message,
                                                         self.queue)

    def on_bindok(self, unused_frame):
        LOGGER.info('QConsumer: Queue bound')
        self.start_consuming()

    def close_channel(self):
        LOGGER.info('QConsumer: Closing the channel')
        self._channel.close()

#------------------------------------------------------------------------------

class QProducer(object):

    def __init__(self, queue, url='amqp://guest:guest@localhost:5672/%2F'):
        self.exchange = 'message'
        self.exchange_type = 'topic'
        self.publish_interval = 1
        self.queue = queue
        self.routing_key = self.queue
        self._connection = None
        self._channel = None
        self._deliveries = []
        self._acked = 0
        self._nacked = 0
        self._message_number = 0
        self._stopping = False
        self._url = url
        self._closing = False
        # connect to rabbit mq
        self._connection = self.connect()

    def connect(self):
        LOGGER.info('QProducer: Connecting to %s', self._url)
        return pika.adapters.TornadoConnection(pika.URLParameters(self._url),
                                               self.on_connection_open)

    def on_connection_open(self, unused_connection):
        LOGGER.info('QProducer: Connection opened')
        self._connection.add_on_close_callback(self.on_connection_closed)
        self.open_channel()

    def open_channel(self):
        LOGGER.info('QProducer: Creating a new channel')
        self._connection.channel(on_open_callback=self.on_channel_open)

    def on_channel_open(self, channel):
        LOGGER.info('QProducer: Channel opened')
        self._channel = channel
        self._channel.add_on_close_callback(self.on_channel_closed)
        self._channel.exchange_declare(self.on_exchange_declareok,
                                       self.exchange,
                                       self.exchange_type)

    def on_exchange_declareok(self, unused_frame):
        LOGGER.info('QProducer: Exchange declared')
        self._channel.queue_declare(self.on_queue_declareok, self.queue)

    def on_queue_declareok(self, method_frame):
        LOGGER.info('QProducer: Binding %s to %s with %s',
                    self.exchange, self.queue, self.routing_key)
        self._channel.queue_bind(self.on_bindok, self.queue,
                                 self.exchange, self.routing_key)

    def on_bindok(self, unused_frame):
        LOGGER.info('QProducer: Queue bound')
        #self._channel.confirm_delivery(self.on_delivery_confirmation)

    def on_delivery_confirmation(self, method_frame):
        confirmation_type = method_frame.method.NAME.split('.')[1].lower()
        LOGGER.info('QProducer: Received %s for delivery tag: %i',
                    confirmation_type,
                    method_frame.method.delivery_tag)
        if confirmation_type == 'ack':
            self._acked += 1
        elif confirmation_type == 'nack':
            self._nacked += 1
        #self._deliveries.remove(method_frame.method.delivery_tag)
        LOGGER.info('QProducer: Published %i messages, %i have yet to be confirmed, '
                    '%i were acked and %i were nacked',
                    self._message_number, len(self._deliveries),
                    self._acked, self._nacked)

    def publish_message(self):
        if self._stopping:
            return

        message = {'test': 'test'}
        properties = pika.BasicProperties(app_id='example-publisher',
                                          content_type='application/json',
                                          headers=message)
        msg = json.dumps(message, ensure_ascii=False)
        self._channel.basic_publish(self.exchange, self.routing_key, msg, properties)
        LOGGER.info('Published message # %s', msg)

    ##############

    def close_connection(self):
        LOGGER.info('QProducer: Closing connection')
        self._closing = True
        self._connection.close()

    def on_connection_closed(self, connection, reply_code, reply_text):
        self._channel = None
        LOGGER.warning('QProducer: Connection closed, reopening in 5 seconds: (%s) %s',
                       reply_code, reply_text)
        self._connection.add_timeout(5, self.reconnect)

    def reconnect(self):
        self._connection = self.connect()

    def on_channel_closed(self, channel, reply_code, reply_text):
        LOGGER.warning('QProducer: Channel was closed: (%s) %s', reply_code, reply_text)
        if not self._closing:
            self._connection.close()

    def close_channel(self):
        LOGGER.info('QProducer: Closing the channel')
        if self._channel:
            self._channel.close()

    
