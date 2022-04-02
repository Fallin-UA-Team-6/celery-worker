import time
from datetime import datetime 

from celery_worker.helpers import get_producer
from celery_worker.types import User, UserId, Cadence
from celery_worker.rmq_apis.consumers import CheckInEventConsumer

def do_test_run():
    now = datetime.utcnow()
    time.sleep(10) # just so last_checkedin_time is noticeably different
    test_timeset_user = User(userId=UserId('sample-tejash-periodic'), 
                    approx_geolocation=Geolocation([47.6038, -122.3301]),
                    last_checkedin_time=now,
                    checkin_algo=now + timedelta(minutes=2)),
                    notifiers=[])

    test_cadence_user = User(userId=UserId('sample-tejash-cadence'), 
                    approx_geolocation=Geolocation([47.6038, -122.3301]),
                    last_checkedin_time=datetime.utcnow(),
                    checkin_algo=Cadence(period=timedelta(minutes=1)),
                    notifiers=[])


    test_timeset_user.add_notifier(test_cadence_user)
    test_cadence_user.add_notifier(test_timeset_user)

    test_timeset_user.set_producer(get_producer(routing_key=str(test_timeset_user.userId)))
    test_cadence_user.set_producer(get_producer(routing_key=str(test_cadence_user.userId)))


    now = datetime.utcnow()
    
    test_timeset_user.checkin()
    test_cadence_user.checkin()


if __name__ == '__main__':
    pass