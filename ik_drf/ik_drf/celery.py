import os

from celery import Celery, signals
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', "ik_drf.settings")

app = Celery('ik_drf')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     # Calls test('hello') every 10 seconds.
#     sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')
#
#     # Calls test('world') every 30 seconds
#     sender.add_periodic_task(30.0, test.s('world'), expires=10)
#
#     # Executes every Monday morning at 7:30 a.m.
#     sender.add_periodic_task(
#         crontab(hour=7, minute=30, day_of_week=1),
#         test.s('Happy Mondays!'),
#     )
#
# @app.task
# def test(arg):
#     print(arg)

app.conf.beat_schedule = {
    'delete_harmful_entries': {
        'task': 'guestbook.tasks.delete_harmful_entries',
        'schedule': crontab(),
    }
}
app.conf.timezone = 'UTC'
