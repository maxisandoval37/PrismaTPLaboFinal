from celery import shared_task
from django.core.mail import send_mail
from time import sleep

from celery import Celery
from celery.schedules import crontab

@shared_task
def sleepy(duration):
    sleep(duration)
    return None


@shared_task
def enviar_correo():
    sleep(10)
    send_mail('ESTO FUNCIONA JODER','AHORA HAY QUE FESTEJAR','tmmzprueba@gmail.com',['jabinot887@dvdoto.com'])
    
    return None



app = Celery()

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(10.0, test.s('Hola!'), name='add every 10')

    # Calls test('world') every 30 seconds
    sender.add_periodic_task(30.0, test.s('Qué buen día, joder!'), expires=10)
    
@app.task
def test(arg):
    print(arg)

@app.task
def add(x, y):
    z = x + y
    print(z)