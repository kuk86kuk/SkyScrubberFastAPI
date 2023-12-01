from celery import Celery

app = Celery('my_celery_tasks', broker='pyamqp://guest@localhost//', backend='rpc://')

@app.task
def my_async_task(arg1, arg2):
    return arg1 + arg2
