from datetime import datetime

import celery
import celery.backends
from celery import Celery

from kombu import Producer, Connection

from celery_worker.logger import logger
from celery_worker.types import UserId
from celery_worker import celeryconfig

from firebase import get_tokens_from_firestore, send_message_to_firebase

app = Celery(config_source=celeryconfig)
queue_name = 'safety-ping-queue'


# class BaseTask(celery.task):
#     def on_failure(self, exc, task_id, args, kwargs, einfo):
#         logging.error(f"Task failed, task_id={task_id} args={args} kwargs={kwargs} exc={exc} einfo={einfo}")
#         self.connection = establish_connection()


@app.task(bind=True)
def notify_to_check_in(self, user_id: UserId, attempt_number: int, time_to_next_checkin: datetime, max_attempts: int = 3) -> None:
    firebase_tokens = get_tokens_from_firestore(user_id)
    logger.info(f'in notifyToCheckIn')
    if attempt_number > max_attempts:
        # notify all the friends using GCS through Firebase
        pass
    else:
        # notify the user "please check in" message
        for token in firebase_tokens:
            send_message_to_firebase(token, {'msg': 'hello! please check in soon'})
        # try the task one more time with the same task_id (that may not be allowed)
        time_to_further_checkin = time_to_next_checkin + timedelta(seconds=10)
        notify_to_check_in.apply_async((user_id, attempt_number+1, time_to_further_checkin), task_id=user_id, eta=time_to_next_checkin)


@app.task(bind=True)
def check_in(self, user_id: UserId, next_checkin_time: str) -> None:
    """
    Reads from RMQ queue about the last checkin of a userId
    Revoke the scheduled celery task that notifies the user about their next checkin with a new time
    """
    logger.info(f'in checkIn')
    # revoke the celery task that notifies the user to check in
    # app.control.revoke(user_id, terminate=False) # trying to revoke ourselves
    # restart the celery task that notifies the user
    time_to_next_checkin = datetime.utcnow() + timedelta(seconds=10)
    notify_to_check_in.apply_async((user_id, 1, time_to_next_checkin), task_id=user_id, eta=datetime.fromisoformat(next_checkin_time[:-1]))
