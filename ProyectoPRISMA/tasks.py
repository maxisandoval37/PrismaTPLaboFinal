from celery import shared_task
from django.core.mail import send_mail
from time import sleep

@shared_task
def sleepy(duration):
    sleep(duration)
    return None


@shared_task
def enviar_correo():
    sleep(10)
    send_mail('ESTO FUNCIONA JODER','AHORA HAY QUE FESTEJAR','tmmzprueba@gmail.com',['jabinot887@dvdoto.com'])
    
    return None
    