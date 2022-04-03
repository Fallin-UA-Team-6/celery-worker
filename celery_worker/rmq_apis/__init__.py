import os

from kombu import Connection, Exchange, Queue

from celery_worker.logger import logger

url = os.getenv('AMQP_URL', 'amqp://localhost:5672/')
pwd = os.getenv('RMQ_PASSWORD', 'password')
user = os.getenv('RMQ_USER', 'username')

# connection = Connection(url)  # no heartbeats set yet, set using heartbeat= param
# channel = connection.channel()
# exchange = Exchange('safety-ping', type='direct')

# from https://medium.com/@Skablam/talking-to-rabbitmq-with-python-and-kombu-6cbee93b1298#.r3ho2468m
def establish_connection():
    revived_connection = connection.clone()
    revived_connection.ensure_connection(max_retries=3)
    channel = revived_connection.channel()
    consumer.revive(channel)
    consumer.consume()
    logger.info('re-connection successful')
    return revived_connection