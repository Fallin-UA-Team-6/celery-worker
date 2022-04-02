from typing import Any

from celery_worker.rmq_apis import connection, channel, establish_connection

from kombu.mixins import ConsumerMixin


def consumer_callback(body, message):
    print(body)  # only print for now
    message.ack()


def init_consumer(queue: str, callback: Any) ->
    consumer = Consumer(connection, queues=queue, callbacks=[process_message], accept=["text/plain"]):  
    consumer.consume()
    # connection.drain_events()
    return consumer


def consume():
    new_conn = establish_connection()
    while True:
        new_conn.drain_events() # shouldn't give socket timeouts


class CheckInEventConsumer(ConsumerMixin):
    def __init__(self, connection, queues):
        self.connection = connection
        self.queues = queues

    def get_consumers(self, Consumer, channel):
        return [Consumer(queues=self.queues,
                         callbacks=[self.on_message])]

    def on_message(self, body, message):
        print('Got message: {0}'.format(body))
        message.ack()
