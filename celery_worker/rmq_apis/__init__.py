import os

from kombu import Connection, Exchange, Producer, Queue

url = os.get('RMQ_URL', 'amqp://localhost:5672/')
pwd = os.get('RMQ_PASSWORD', 'password')
user = os.get('RMQ_USER', 'username')

connection = Connection(f'{user}:{pwd}@{url}')  # no heartbeats set yet, set using heartbeat= param
channel = conn.channel
exchange = Exchange('safety-ping', type='direct')


def establish_connection():
    revived_connection = conn.clone()
    revived_connection.ensure_connection(max_retries=3)
    channel = revived_connection.channel()
    consumer.revive(channel)
    consumer.consume()
    return revived_connection