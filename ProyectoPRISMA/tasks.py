from item.models import Item, Pedidos, Proveedor, Sucursal
from celery import shared_task, Celery
from django.core.mail import send_mail
from time import sleep
import random
from usuario.models import Supervisor


@shared_task
def sleepy(duration):
    sleep(duration)
    return None


@shared_task
def Pedido():
    itemsToSentToSupervisores = Item.objects.raw("""
        SELECT *
        FROM item_item
        WHERE cantidad <= stockseguridad
    """)

    itemsBySucursal = {}
    for item in itemsToSentToSupervisores:
        if not itemsBySucursal.__contains__(item.sucursal_id):
            itemsBySucursal.update({item.sucursal_id: []})
        itemsBySucursal.get(item.sucursal_id).append("- " + str(item.nombre))

    print('****itemsBySucursal: ')
    print(itemsBySucursal)

    supervisores = Supervisor.objects.raw("""
        SELECT *
        FROM usuario_supervisor
        WHERE sucursal_id IN %s
    """, [tuple(list(itemsBySucursal.keys()))])

    supervisorAlreadyListened = []
    for supervisor in supervisores:
        if supervisor.id not in supervisorAlreadyListened:
            send_mail('ÍTEMS SIN STOCK - SUCURSAL ' + str(supervisor.sucursal_id), "Buenas tardes " + supervisor.nombre + ", a continuación se listan los ítems cuyo stock de riesgo ha sido alcanzado:\n" +
                      '\n'.join(itemsBySucursal.get(supervisor.sucursal_id)), 'tmmzprueba@gmail.com', {supervisor.email})
            supervisorAlreadyListened.append(supervisor.id)

    items = Item.objects.raw("""
        SELECT *
        FROM item_item
        WHERE cantidad <= stockminimo
    """)

    proveedoresQuery = Proveedor.objects.raw("""
        SELECT id, email 
        FROM proveedor_proveedor
        LIMIT 10
    """)

    proveedoresEmails = []
    for proveedor in proveedoresQuery:
        proveedoresEmails.append(proveedor.email)

    itemsToChangeProveedor = {}

    for item in items:
        print('****item: ' + str(item))
        print('****item.reintentos: ' + str(item.reintentos))
        if item.solicitud == False:
            item.solicitud = True
            item.save()
            pedido = Pedidos()
            pedido.item = item
            pedido.sucursal = item.sucursal
            pedido.proveedor = item.categoria.prov_preferido
            print(item.repo_por_lote)
            if item.repo_por_lote:
                pedido.cantidad = item.cantidad_lote
            pedido.save()
        elif(item.reintentos < 2):
            item.reintentos += 1
            item.save()
        else:
            print('****The OLD proveedor is: ' +
                  str(item.categoria.prov_preferido.email))
            indice = proveedoresEmails.index(
                item.categoria.prov_preferido.email)
            if indice == 0:
                print('****The NEW proveedor is: ' + str(list(proveedoresQuery)
                                                         [(random.randint(1, len(list(proveedoresQuery)) - 1))].email))
                itemsToChangeProveedor.update({item.id: list(proveedoresQuery)[(
                    random.randint(1, len(list(proveedoresQuery)) - 1))].email})
            elif indice == len(list(proveedoresQuery)):
                print('****The NEW proveedor is: ' + str(list(proveedoresQuery)
                                                         [(random.randint(0, len(list(proveedoresQuery)) - 2))].email))
                itemsToChangeProveedor.update({item.id: list(proveedoresQuery)[(
                    random.randint(0, len(list(proveedoresQuery)) - 2))].email})
            else:
                print('****The NEW proveedor is: ' + str(list(proveedoresQuery)
                                                         [(random.randint(0, indice - 1))].email))
                itemsToChangeProveedor.update(
                    {item.id: list(proveedoresQuery)[(random.randint(0, indice - 1))].email})
            item.reintentos = 0
            item.save()

    pedidos = Pedidos.objects.raw("""
        SELECT id, item_id, proveedor_id, sucursal_id
        FROM item_pedidos        
    """)

    alreadyListened = []
    emailsByProveedores = {}
    proveedores = []
    for pedido in pedidos:
        proveedores.append(str(pedido.proveedor_id))

    print(proveedores)

    proveedores = Proveedor.objects.raw("""
        SELECT id, email 
        FROM proveedor_proveedor 
        WHERE id IN %s
        """, [tuple(proveedores)])

    for proveedor in proveedores:
        emailsByProveedores.setdefault(proveedor.id, proveedor.email)

    for pedido in pedidos:
        if pedido not in alreadyListened and not itemsToChangeProveedor.__contains__(pedido.id):
            send_mail('SOLICITUD DE STOCK - SUCURSAL ' + str(pedido.sucursal_id), "Buenas tardes, esta es una solicitud de stock automática. Por favor, diríjase al siguiente link para indicar las cantidades que nos puede proveer de cada ítem:\n" +
                      "http://127.0.0.1:8000/items/pedido_proveedor/" + str(pedido.proveedor_id) + "/" + str(pedido.sucursal_id), 'tmmzprueba@gmail.com', {emailsByProveedores.get(pedido.proveedor_id)})
            alreadyListened.append(pedido)
        elif pedido not in alreadyListened and itemsToChangeProveedor.__contains__(pedido.id):
            send_mail('SOLICITUD DE STOCK - SUCURSAL ' + str(pedido.sucursal_id), "Buenas tardes, esta es una solicitud de stock automática. Por favor, diríjase al siguiente link para indicar las cantidades que nos puede proveer de cada ítem:\n" +
                      "http://127.0.0.1:8000/items/pedido_proveedor/" + str(pedido.proveedor_id) + "/" + str(pedido.sucursal_id), 'tmmzprueba@gmail.com', {itemsToChangeProveedor.get(pedido.id)})
            alreadyListened.append(pedido)

    return None


app = Celery()






