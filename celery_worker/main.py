from datetime import datetime

from celery import Celery

from kombu import Producer, Connection

from celery_worker.rmq_apis import connection, establish_connection, url
from celery_worker.rmq_apis.helpers import get_producer
from celery_worker.types import UserId

app = Celery('safety-ping', backend='amqp', broker=connection)
queue_name = 'safety-ping-queue'


class BaseTask(celery.task):
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logging.error(f"Task failed, task_id={task_id} args={args} kwargs={kwargs} exc={exc} einfo={einfo}")
        self.connection = establish_connection()

@app.task(bind=True)
def check_in(self, user_id: UserId, next_checkin_time: datetime) -> None:
        """
        Reads from RMQ queue about the last checkin of a userId
        Revoke the scheduled celery task that notifies the user about their next checkin with a new time
        """
        self.name = 'checkIn'
        self._producer = Producer(Connection(url))
        self.user_id = kwargs.get('user_id')
        notifyToCheckIn_task_id = f'{user_id}-notifyToCheckIn'
        # revoke the celery task that notifies the user to check in
        app.control.revoke(notifyToCheckIn_task_id, terminate=True)
        # restart the celery task that notifies the user
        app.register(NotifyToCheckIn(user_id=user_id, attempt_number=1), 
                    task_id=notifyToCheckIn_task_id)
        self._producer.close()


@app.task(bind=True)
def notify_to_check_in(self, user_id: UserId, attempt_number: int, max_attempts: int = 3) -> None:
    name = 'notifyToCheckIn'

    self.user_id = kwargs.get('user_id')
        if attempt_number > max_attempts:
            # notify all the relatives using GCS through Firebase
            pass
        else:
            # try one more time with the same task_id (that may not be allowed)
            app.register(NotifyToCheckIn(user_id=user_id, attempt_number=attempt_number+1),
                                        task_id=self.task_id)
    