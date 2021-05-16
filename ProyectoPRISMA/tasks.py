from celery import shared_task
from django.core.mail import send_mail
from time import sleep
import json
from celery import Celery
from celery.schedules import crontab
from item.models import Item, Pedidos
from django.db.models import F

@shared_task
def sleepy(duration):
    sleep(duration)
    return None



@shared_task
def Pedido(email):

    queryset = Item.objects.filter(cantidad=F('stockMinimo'))
    
    for item in queryset:
        if item.solicitud == False:
            pedidos = Pedidos()
            pedidos.item = item
            pedidos.sucursal = item.sucursal
            pedidos.proveedor = item.categoria.prov_preferido

            pedidos.save()
           
        item.solicitud = True
        item.save()

    pedidosByProveedores = {};

    resultado = Pedidos.objects.raw("""
        SELECT id, item_id, proveedor_id, sucursal_id 
        FROM item_pedidos
        """)
    
    for pedido in resultado:
        alreadyListened = []
        pedidosByProveedores.setdefault(pedido.proveedor_id, []).append(pedido)

    
    for pedido in resultado:
        pedidosToSend = []
        for elPedido in pedidosByProveedores.get(pedido.proveedor_id):
            if(pedido.sucursal_id == elPedido.sucursal_id and elPedido not in alreadyListened):
                pedidosToSend.append(elPedido)
                alreadyListened.append(elPedido)
       # print(pedidosToSend) # envio al proveedor
    contenido = ""
    for info in pedidosToSend:
           contenido += "  " + str(info) + " "
    
    
    send_mail('CORREO PARA PROVEEDOR', str(pedidosToSend), 'tmmzprueba@gmail.com', {email})
    
    return None

""" @shared_task
def enviar_correo(email):
    
    lista = Pedido()
    print(lista)
    send_mail('FUNCIONA JODER', 'CHUPAME LAS BOLAS DE FELPA', 'tmmzprueba@gmail.com', {email})

    return None """

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
    
    
