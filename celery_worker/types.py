from types import NewType, Tuple, Set

from pydantic import BaseModel
from datetime import datetime, timedelta


UserId = NewType('UserId', str)
Geolocation = NewType('Geolocation', Tuple[float, float])

class Cadence(BaseModel):
    period: timedelta


class User(BaseModel):
    userId: UserId
    approx_geolocation: Geolocation
    last_checkedin_time: datetime
    checkin_algo: Any[Cadence, datetime]  # either decides to check in periodically or next check in is at a time
    notifiers: Optional[Set[User]]
    producer: Optional[Producer] = None 

    @property
    def next_checkin_time(self) -> datetime
        if self.checkin_algo.isinstance(Cadence):
            return self.last_checkedin_time + self.checkin_algo.period
        else:
            return self.checkin_algo

    def add_notifier(self, notifier: User):
        self.notifiers.add(notifier)

    def checkin(self, checkin_time: datetime):
        self.last_checkedin_time = checkin_time

    def set_producer(self, producer: Producer):
        self.producer = producer


class UserChecksInEvent:
    userId: UserId
    utc_time: datetime
