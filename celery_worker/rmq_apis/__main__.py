import time
from datetime import datetime, timedelta

from kombu import Queue

from celery_worker.types import User, UserId, Cadence, Geolocation
from celery_worker.rmq_apis import connection, exchange
from celery_worker.rmq_apis.helpers import get_producer
from celery_worker.rmq_apis.consumers import CheckInEventConsumer

def run_consumers():
    pass


def do_test_run():
    now = datetime.utcnow()
    time.sleep(10) # just so last_checkedin_time is noticeably different
    test_timeset_user = User(userId=UserId('sample-tejash-periodic'), 
                            approx_geolocation=Geolocation([47.6038, -122.3301]),
                            last_checkedin_time=now,
                            checkin_algo=now + timedelta(minutes=2),
                            notifiers=[])

    test_cadence_user = User(userId=UserId('sample-tejash-cadence'), 
                    approx_geolocation=Geolocation([47.6038, -122.3301]),
                    last_checkedin_time=datetime.utcnow(),
                    checkin_algo=Cadence(period=timedelta(minutes=1)),
                    notifiers=[])

    test_timeset_user.add_notifier(test_cadence_user.userId)
    test_cadence_user.add_notifier(test_timeset_user.userId)

    test_timeset_user.set_producer(get_producer(routing_key=str(test_timeset_user.userId)))
    test_cadence_user.set_producer(get_producer(routing_key=str(test_cadence_user.userId)))


    now = datetime.utcnow()
    geoloc = Geolocation([37.7749300, -122.4194200])
    
    test_timeset_user.checkin(checkin_time=now, approx_geolocation=geoloc)
    test_cadence_user.checkin(checkin_time=now, approx_geolocation=geoloc)
    print('forming queues')

    queues = [Queue(name=user.userId, exchange=exchange, routing_key=user.userId) for user in [test_timeset_user, test_cadence_user]]

    consumer = CheckInEventConsumer(connection, queues)
    consumer.run()

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser(description='rabbit mq functionality for safety-ping app')
    subparsers = parser.add_subparsers(dest='subcommand', help='sub-commands', required=True)

    parser_test = subparsers.add_parser('test', help='run a test')
    parser_run = subparsers.add_parser('run', help='the command to run')
    args = parser.parse_args()


    if args.subcommand == 'test':
        print('doing a test run now...')
        do_test_run()
    elif args.subcommand == 'run':
        print('running the rabbit MQ workflow now...')
        pass