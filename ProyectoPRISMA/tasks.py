from celery import shared_task
from django.core.mail import send_mail
from time import sleep
import json
from celery import Celery
from celery.schedules import crontab
from item.models import Item, Pedidos, Proveedor
from django.db.models import F

@shared_task
def sleepy(duration):
    sleep(duration)
    return None



@shared_task
def Pedido(email):
    queryset = Item.objects.filter(cantidad=F('stockMinimo'))
    # pedidosToSend = []
    for item in queryset:
        if item.solicitud == False:
            pedidos = Pedidos()
            pedidos.item = item
            pedidos.sucursal = item.sucursal
            pedidos.proveedor = item.categoria.prov_preferido

            pedidos.save()
           
        item.solicitud = True
        item.save()

    resultado = Pedidos.objects.raw("""
        SELECT id, item_id, proveedor_id, sucursal_id 
        FROM item_pedidos
        """)

    alreadyListened = []
    emailsByProveedores = {}
    proveedores = []
    for pedido in resultado:
        proveedores.append(str(pedido.proveedor_id))
    print(proveedores)
    proveedores = Proveedor.objects.raw("""
        SELECT id, email 
        FROM proveedor_proveedor 
        WHERE id IN %s
        """, [tuple(proveedores)])

    for proveedor in proveedores:
        emailsByProveedores.setdefault(proveedor.id, proveedor.email)

    for pedido in resultado:
        if(pedido not in alreadyListened):
            send_mail('SOLICITUD DE STOCK - SUCURSAL ' + str(pedido.sucursal_id), "Buenas tardes, esta es una solicitud de stock automática. Por favor, diríjase al siguiente link para indicar las cantidades que nos puede proveer de cada ítem:\n" + "http://localhost:8000/items/pedido_proveedor/" + str(pedido.proveedor_id) + "/" + str(pedido.sucursal_id), 'tmmzprueba@gmail.com', {emailsByProveedores.get(pedido.proveedor_id)})
            alreadyListened.append(pedido)
    
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
    
