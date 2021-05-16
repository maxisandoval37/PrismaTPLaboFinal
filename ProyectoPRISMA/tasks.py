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
def enviar_correo(email):
    
    send_mail('FUNCIONA JODER', 'CHUPAME LAS BOLAS DE FELPA', 'tmmzprueba@gmail.com', {email})

    return None

app = Celery()

@shared_task
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(10.0, test.s('Hola!'), name='add every 10')

@app.task
def test(arg):
    print(arg)

@app.task
def add(x, y):
    z = x + y
    print(z)