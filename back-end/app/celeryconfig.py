broker_url='redis://127.0.0.1:6379/1'
result_backend='redis://127.0.0.1:6379/2'

from celery.schedules import crontab


beat_schedule = {
    'check-price-every-hour': {
        'task': 'alert',
        # 'schedule': crontab(minute='*/1'),
        'schedule': crontab(minute=0, hour='*'),  # 每小时执行一次
    },
}