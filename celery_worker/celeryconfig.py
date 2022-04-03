import os

url = os.getenv('AMQP_URL', 'amqp://localhost:5672/')
user = os.getenv('RMQ_USER', 'username')

broker_transport_options = {
    'queue_name_prefix': 'safety-ping',
}

transport = {
    'url': 'rabbitmq'
}

task_default_queue = 'safety-ping'
broker_url = url
result_backend = url
username = user
