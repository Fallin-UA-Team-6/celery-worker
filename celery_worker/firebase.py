import os
import firebase_admin
from firebase_admin import credentials, messaging

import firebase_admin.firestore
from firebase_admin.firestore import Transaction, Query

from celery_worker.types import UserId

cred = credentials.Certificate(f"{os.path.expanduser('~')}/secret")
should_init_app = True
if should_init_app:
    app = firebase_admin.initialize_app(cred)
    should_init_app = False


firestore_client = firebase_admin.firestore.client(app)

def send_message_to_firebase(token: str, data: dict) -> None:
    msg = messaging.Message(data=data, token=token)
    messaging.send(msg)

def get_tokens_from_firestore(user_id: UserId) -> str:
    user_token_collection = firestore_client.collection('user_tokens')
    query_ref = user_token_collection.where(u'uid', u'==', user_id)
    for doc in query_ref.stream():
        return doc.to_dict()['tokens']  # return first, should only be one
