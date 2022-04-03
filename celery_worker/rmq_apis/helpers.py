import os
from typing import Optional

from kombu import Exchange, Producer, Queue

from celery_worker.rmq_apis import connection, channel, exchange


def get_producer(routing_key: Optional[str] = None) -> Producer:
    return Producer(exchange=exchange, channel=channel, routing_key=routing_key)


def get_queue(routing_key: str, name: Optional[str] = None) -> Queue:
    if not name:
        name = f'queue-{routing_key}'

    queue = Queue(name=name, exchange=exchange, routing_key=routing_key)
    queue.maybe_bind(connection)
    queue.declare()
    return queue

