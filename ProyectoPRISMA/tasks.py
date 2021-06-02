from item.models import Item, Pedidos, Proveedor
from venta.models import Venta, ItemVenta, EstadoVenta
from celery import shared_task, Celery
from django.core.mail import send_mail
from usuario.models import Supervisor
from cliente.models import Cliente
from sucursal.models import Caja
from decimal import Decimal
from datetime import date
from time import sleep
import random
import json
from django.db.models import Count

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
                pedido.cantidad = item.cantidad_lote * 2
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


@shared_task
def receiveVentasVirtuales():
    #body = open('body.json',)
    body = """{
    "ventas": [
        {
            "numero_comprobante": "12500",
            "cliente_asociado_id": "2",
            "cuenta_corriente_id": "2",
            "estado_id": "5",
            "mediopago_id": "2",
            "sucursal_asociada_id": "1",
            "vendedor_asociado_id": "6",
            "tipo_de_venta":"VIRTUAL",
            "items": [
                {
                    "item_id": "1",
                    "cantidad_solicitada": "5",
                    "monto": "1200,00",
                    "sucursal_asociada_id": "1",
                    "venta_asociada_id": "1"
                }
                
            ]
        }

    ]
}"""

    # print('****************')
    for i in range(0, len(json.loads(body)['ventas'])):
        venta = json.loads(body)['ventas'][i]
        numero_comprobante = venta['numero_comprobante']
        cliente_asociado_id = venta['cliente_asociado_id']
        cuenta_corriente_id = venta['cuenta_corriente_id']
        estado_id = venta['estado_id']
        mediopago_id = venta['mediopago_id']
        sucursal_asociada_id = venta['sucursal_asociada_id']
        vendedor_asociado_id = venta['vendedor_asociado_id']
        tipo_de_venta = venta['tipo_de_venta']
        # print('****************')
        # print('Venta: ' + str(i))
        # print('numero_comprobante: ' + numero_comprobante)
        # print('cliente_asociado_id: ' + cliente_asociado_id)
        # print('cuenta_corriente_id: ' + cuenta_corriente_id)
        # print('estado_id: ' + estado_id)
        # print('mediopago_id: ' + mediopago_id)
        # print('sucursal_asociada_id: ' + sucursal_asociada_id)
        # print('vendedor_asociado_id: ' + vendedor_asociado_id)

        try:
            ventaToInsert = Venta()
            ventaToInsert.numero_comprobante = int(numero_comprobante)
            ventaToInsert.cliente_asociado_id = int(cliente_asociado_id)
            ventaToInsert.vendedor_asociado_id = int(vendedor_asociado_id)
            ventaToInsert.sucursal_asociada_id = int(sucursal_asociada_id)
            ventaToInsert.mediodepago_id = int(mediopago_id)
            ventaToInsert.cuenta_corriente_id = int(cuenta_corriente_id)
            ventaToInsert.estado_id = int(estado_id)
            ventaToInsert.tipo_de_venta = str(tipo_de_venta)
            ventaToInsert.save()
        except Exception as e:
            print("Exception:")
            print(e)

        # print('****************')
        for k in range(0, len(venta['items'])):
            item = venta['items'][k]
            print('\titem_venta: ' + str(k))
            cargarItemVenta(item, numero_comprobante)

     #print('****************')

    #body.close()

    return None


def cargarItemVenta(objeto, numero_comprobante):
    ventaFromQuery = Venta.objects.raw("""
        SELECT id
        FROM venta_venta
        WHERE numero_comprobante = %s
    """, [str(numero_comprobante)])

    for v in ventaFromQuery:
        venta = v.id

    lista_items = []
    lista_ventas = []
    item = objeto['item_id']
    cantidad = objeto['cantidad_solicitada']
    sucursal = objeto['sucursal_asociada_id']
    precio = objeto['monto']

    # print('\titem: ' + item)
    # print('\tcantidad: ' + cantidad)
    # print('\tprecio: ' + precio)
    # print('\tsucursal: ' + sucursal)
    # print('\tventa: ' + str(venta))

    item_venta = ItemVenta()
    item_venta.item_id = int(item)
    item_venta.cantidad_solicitada = int(cantidad)
    item_venta.sucursal_asociada_id = str(sucursal)
    item_venta.venta_asociada_id = int(venta)
    item_venta.monto = Decimal(cantidad.replace(
        ',', '.')) * Decimal(precio.replace(',', '.'))

    lista_items.append(item_venta.item_id)
    lista_ventas.append(item_venta.venta_asociada_id)

    item_venta.save()

    item_de_venta = Item.objects.raw("""
        SELECT * 
        FROM item_item 
        WHERE id IN %s               
    """, [tuple(lista_items)])

    for item in item_de_venta:
        item.cantidad -= item_venta.cantidad_solicitada
        item.save()

    ventas = Venta.objects.raw("""
        SELECT * 
        FROM venta_venta
        WHERE id IN %s               
    """, [tuple(lista_ventas)])

    for venta in ventas:
        venta.total += item_venta.monto
        venta.save()

    return None


@shared_task
def enviarAvisoDisposicion():
    ventas = Venta.objects.raw("""
        SELECT *
        FROM venta_venta
    """)

    ventasAAvisar = []
    ventasADisponer = []

    for venta in ventas:
        print("DIAS: " + str(abs(date.today() - venta.fecha.date()).days))
        if venta.estado.opciones == EstadoVenta.opcionesVenta.PENDIENTE_DE_RETIRO and abs(date.today() - venta.fecha.date()).days == 7:
            ventasAAvisar.append(venta)
        elif venta.estado.opciones == EstadoVenta.opcionesVenta.PENDIENTE_DE_RETIRO and abs(date.today() - venta.fecha.date()).days == 8:
            ventasADisponer.append(venta)

    print("ventasAAvisar: ")
    print(ventasAAvisar)

    print("ventasADisponer: ")
    print(ventasADisponer)

    for venta in ventasAAvisar:
        print("ENVIANDO EMAIL")
        send_mail('AVISO DISPOSICIÓN DE COMPRA - ' + venta.cliente_asociado.nombre, "Buenas tardes, " + venta.cliente_asociado.nombre + " este es un aviso automático de que su venta realizada el " + str(venta.fecha.date()) +
                  " va a ser dispuesta. Por favor, diríjase a la sucursal N°" + str(venta.sucursal_asociada_id) + " dentro de las siguientes 24hs para poder retirarla.\nDe otra forma, se le devolverá sólo el 75" + '%' + " de su dinero.\n\n--\nSaludos.", 'tmmzprueba@gmail.com', {venta.cliente_asociado.email})

    ids = EstadoVenta.objects.filter(opciones = 'NO RETIRADA')
    nuevo_estado = ""
    for id in ids:
        
        nuevo_estado = id.id

    for venta in ventasADisponer:
        
        
        cajas = Caja.objects.filter(sucursal_id = venta.sucursal_asociada_id)
        venta.estado_id = nuevo_estado
        venta.save()
        
        for caja in cajas:
            
            caja.saldo_disponible += (venta.total * Decimal("0.75".replace(',', '.')))
            caja.save()
            
            break
        
    return None

@shared_task()
def ListaItemsPorCriterio():
    
    items_venta = ItemVenta.objects.values('item_id').annotate(Count('item_id')).order_by()[:5]
    items = []
    
    for item in items_venta:
        items.append(item.get('item_id'))
        
    item_obtenido = Item.objects.raw("""
    SELECT *
    FROM item_item
    WHERE id IN %s                                                                                 
    """, [tuple(items)])
    
    for item in item_obtenido:
        
        item.stockminimo = 10
        item.stockseguridad = 5
        item.save()
     

app = Celery()
