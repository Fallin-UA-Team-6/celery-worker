import json
from typing import Any

from celery_worker.logger import logger
from celery_worker.rmq_apis import connection, channel, establish_connection

from kombu import Consumer
from kombu.mixins import ConsumerMixin


class CheckInEventConsumer(ConsumerMixin):
    def __init__(self, connection, queues):
        self.connection = connection
        self.queues = queues
        logger.info(f'created consumer with {self.queues}')

    def get_consumers(self, Consumer, channel):
        return [Consumer(queues=self.queues,
                         callbacks=[self.on_message],
                         accept=['text/json', 'text/plain'])]

    def on_message(self, body, message):
        try:
            logger.info(f'Got message: {json.loads(body)}')
        except json.decoder.JSONDecodeError:
            logger.info(f'Got message: {body}')
        message.ack()
