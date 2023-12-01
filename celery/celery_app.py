from celery import Celery

app = Celery(
    'my_celery_app',
    broker='pyamqp://guest@localhost//',
    backend='rpc://'
)

