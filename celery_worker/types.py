from typing import NewType, Tuple, Set, Union, Optional, Any

from pydantic import BaseModel
from datetime import datetime, timedelta

from kombu import Producer

from celery_worker.logger import logger
# from celery_worker.rmq_apis import exchange

UserId = NewType('UserId', str)
Geolocation = NewType('Geolocation', Tuple[float, float])

class RMQMessage(BaseModel):
    checkin_time: datetime
    geoloc: Geolocation


class Cadence(BaseModel):
    period: timedelta


class User(BaseModel):
    userId: UserId
    approx_geolocation: Geolocation
    last_checkedin_time: datetime
    checkin_algo: Union[Cadence, datetime]  # either decides to check in periodically or next check in is at a time
    notifiers: Optional[Set[UserId]]
    producer: Optional[Any] = None 

    @property
    def next_checkin_time(self) -> datetime:
        if self.checkin_algo.isinstance(Cadence):
            return self.last_checkedin_time + self.checkin_algo.period
        else:
            return self.checkin_algo

    def add_notifier(self, notifier: UserId):
        self.notifiers.add(notifier)

    def set_producer(self, producer: Any):
        self.producer = producer

    def checkin(self, checkin_time: datetime, approx_geolocation: Geolocation):
        msg = RMQMessage(checkin_time=checkin_time, geoloc=approx_geolocation)
        self.producer.publish(msg.json(), exchange=exchange, routing_key=str(self.userId)) # throws error if producer is not set
        self.last_checkedin_time = checkin_time
        self.approx_geolocation = approx_geolocation
        self.producer.close()
        logger.info(f'published {msg.json()}')


class UserChecksInEvent:
    userId: UserId
    utc_time: datetime
