from celery import Celery
import os
from celery.schedules import crontab

app = Celery('ProyectoPRISMA',
             broker='amqp://localhost',
             backend='rpc://',
             include=['ProyectoPRISMA.tasks'])


# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ProyectoPRISMA.settings.local')
SECRET_KEY = '0=k(5)!gnn(3p#z=&%tg7_^t^tz)2mfd24y=4xv96v4w0qe^3h'
app = Celery('ProyectoPRISMA')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a CELERY_ prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')


app.conf.beat_schedule = {
    'cada-24-horas': {  #cada dia a las 18:00 cuando cierra la caja
        'task': 'ProyectoPRISMA.tasks.Pedido',
        'schedule': crontab(hour=18, minute=00),
        'args': ('fasami6970@o3live.com',)
    },
}

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
    task_serializer='json',
    accept_content=['json'],  # Ignore other content
    result_serializer='json',
    enable_utc=True,
)

if __name__ == '__main__':
    app.start()