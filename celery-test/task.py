import time
from celery import Celery

app = Celery('tasks', broker='redis://localhost:6379/2')

@app.task
def add(x, y):
    time.sleep(1)
    return x + y
