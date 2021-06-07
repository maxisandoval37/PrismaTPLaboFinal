from django.shortcuts import render, HttpResponseRedirect, redirect
from .forms import VentaLocalForm, VentaVirtualForm, ItemVentaForm
from .models import EstadoVenta, VentaLocal, VentaVirtual, Venta, ItemVenta
from django.views.generic import  CreateView,  DeleteView, ListView
from usuario.mixins import ValidarLoginYPermisosRequeridos
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import ProtectedError
from cliente.models import Cliente, CuentaCorriente,MedioDePago
from sucursal.models import Sucursal, Caja, Operacion
from usuario.models import Vendedor
from item.models import Item, Estado
from django.http import HttpResponse, HttpResponseBadRequest
from decimal import Decimal
import json
from django.contrib.messages.views import SuccessMessageMixin

class ListadoVenta(ValidarLoginYPermisosRequeridos,ListView):
    
    permission_required = ('venta.view_venta',)
    model = Venta
    template_name = 'ventas/listar_venta.html'

class ListadoVentaCajero(ValidarLoginYPermisosRequeridos,ListView):
    
    permission_required = ('venta.view_venta_cajero',)
    model = Venta 
    template_name = 'ventas/listar_venta_cajero.html'
    #queryset = Venta.objects.filter(estado_id = 2)

class RegistrarVentaLocal(ValidarLoginYPermisosRequeridos,SuccessMessageMixin,CreateView):
    
    permission_required = ('venta.view_venta','venta.add_venta',)
    model = VentaLocal
    context_object_name = 'obj'
    form_class = VentaLocalForm
    template_name = 'ventas/crear_venta_local.html'
    success_url = reverse_lazy('ventas:listar_ventas')
    success_message = 'Venta local registrada correctamente.'
      
    
    def get_context_data(self, **kwargs):
        context = super(RegistrarVentaLocal, self).get_context_data(**kwargs)
        context["cliente_asociado"] = Cliente.objects.all()
        context["mediodepago"] = MedioDePago.objects.all()
        context["cuenta_corriente"] = CuentaCorriente.objects.all()
        context["sucursal_asociada"] = Sucursal.objects.all()
        context["vendedor_asociado"] = Vendedor.objects.all()
        return context
    
    
    
    
class RegistrarVentaVirtual(ValidarLoginYPermisosRequeridos,SuccessMessageMixin,CreateView):
    
    permission_required = ('venta.view_venta','venta.add_venta',)
    model = VentaVirtual
    context_object_name = 'obj'
    form_class = VentaVirtualForm
    template_name = 'ventas/crear_venta_virtual.html'
    success_url = reverse_lazy('ventas:listar_ventas')
    success_message = 'Venta virtual registrada correctamente.'
    
    def get_context_data(self, **kwargs):
        context = super(RegistrarVentaVirtual, self).get_context_data(**kwargs)
        context["cliente_asociado"] = Cliente.objects.all()
        context["mediodepago"] = MedioDePago.objects.all()
        context["cuenta_corriente"] = CuentaCorriente.objects.all()
        context["sucursal_asociada"] = Sucursal.objects.all()
        context["vendedor_asociado"] = Vendedor.objects.all()
        return context
    
class EliminarVenta(ValidarLoginYPermisosRequeridos,SuccessMessageMixin,DeleteView):
    
    permission_required = ('venta.view_venta','venta.delete_venta',)
    model = Venta
    template_name = 'ventas/eliminar_venta.html'
    success_url = reverse_lazy('ventas:listar_ventas')
    success_message = 'Se eliminó la venta correctamente.'
                                    
    def delete(self, request, *args, **kwargs):
        
        self.object = self.get_object()
        success_url = self.get_success_url()

        try:
            self.object.delete()
        except ProtectedError:
            messages.add_message(request, messages.ERROR, 'No se puede eliminar: Ésta venta está relacionada.')
            return redirect('ventas:listar_ventas')

        return HttpResponseRedirect(success_url)                                
    
    

def ListarItem(request, venta):
    
    
    items = ItemVenta.objects.filter(venta_asociada = venta)
   
    lista = []
    for item in items:
        
        lista.append(item)
   
    return render(request, 'ventas/listar_itemventa.html', locals())

def VerItems(request, venta):
    
    
    items = ItemVenta.objects.filter(venta_asociada = venta)
   
    lista = []
    for item in items:
        
        lista.append(item)
   
    return render(request, 'ventas/ver_items.html', locals())
        
        
def VerDetalle(request, sucursal, venta):
    
   
    sucursal = Sucursal.objects.get(id = sucursal)
    estados = Estado.objects.filter(opciones = 'ACTIVO')
    nuevo_estado = 0
    for estado in estados:
        nuevo_estado = estado.id
    
    queryset = Item.objects.filter(sucursal = sucursal.id, estado = nuevo_estado)
    lista = []
    for item in queryset:
        dic = {
            "nombre": item.nombre,
            "categoria": item.categoria,
            "precio": item.precio,
            "estado": item.estado,
            "unidad": item.unidad_de_medida,
            "ubicacion": item.ubicacion,
            "id": item.id,
            "sucursal": item.sucursal,
            "venta": venta,
            
        }
        lista.append(dic)
         
   
    
    return render(request, 'ventas/crear_itemventa.html',locals())


def AgregarItem(request, sucursal, venta):
    
    
    if request.is_ajax():
        object = json.loads(request.POST.get('items'))
        
        lista_items = []
        lista_ventas = []
        lista_errores = []
        lista_success = []
        
        for info in object:
            objeto = json.loads(info)
            
            item = objeto['item']
            cantidad = objeto['cantidad']
            sucursal = objeto['sucursal']
            venta = objeto['venta']
            precio = objeto['precio']
            
            item_venta = ItemVenta()
            item_venta.item_id = int(item)
            
            if cantidad == "":
                return HttpResponseBadRequest()
            else:
                item_venta.cantidad_solicitada = int(cantidad)
                
            item_venta.sucursal_asociada_id = str(sucursal)
            item_venta.venta_asociada_id = int(venta)
            item_venta.monto = Decimal(cantidad.replace(',', '.')) * Decimal(precio.replace(',', '.'))
            
            
            
            validacion = validar(request, item_venta)
            
            if validacion != None:
                lista_errores.append(validacion)
                continue
            else:
                lista_success.append(item_venta.item.nombre)
            
            lista_items.append(item_venta.item_id)
            lista_ventas.append(item_venta.venta_asociada_id)
            
            print(lista_success)
            print(lista_errores)
            item_venta.save()
            
            queryset = Venta.objects.raw("""
                SELECT * 
                FROM venta_venta
                WHERE numero_comprobante IN %s               
            """, [tuple(lista_ventas)])  
            
            
            for venta in queryset:
                
                venta.total += item_venta.monto
               
                venta.save()
        
        
            if len(lista_items) > 0:
                item_de_venta = Item.objects.raw("""
                    SELECT * 
                    FROM item_item 
                    WHERE id IN %s               
                """, [tuple(lista_items)])  
                
                
                for item in item_de_venta:
                    print(item_venta.cantidad_solicitada)
                    if (item.cantidad - item_venta.cantidad_solicitada) < 0:
                        return HttpResponseBadRequest()
                    else:
                        
                        item.cantidad -= item_venta.cantidad_solicitada
                        item.save() 
                
            
        mensaje = "Se añadieron: "
        for m in lista_success:
            mensaje += m + ", "
        if len(lista_success) == 0:    
            mensaje = "No se añadieron: "
        else:
            mensaje = mensaje[0:len(mensaje)-2] + ".\nNo se añadieron: "
            
        for m in lista_errores:
            mensaje += m + ", "
        
        if len(lista_errores) == 0:
            mensaje = mensaje[0:len(mensaje)-18] 
        else:
            mensaje = mensaje[0:len(mensaje)-2] + "."
        #messages.success(request, "Item agregado correctamente.")
        return HttpResponse(mensaje)
    

def validar(request, item_venta):
    
    if item_venta.item.cantidad == 0:
            #messages.error(request, "No hay stock del item solicitado.")
            return item_venta.item.nombre + " (No hay stock del item solicitado)"
        
        
    if item_venta.venta_asociada.cliente_asociado.nombre == 'CONSUMIDOR FINAL' and item_venta.item.precio >= 10000:
        
         #messages.error(request, "Es necesario registrar al cliente para agregar el item.")
         return item_venta.item.nombre + " (Es necesario registrar al cliente para agregar el item)"
    
    
    if item_venta.item.cantidad < item_venta.cantidad_solicitada:
        #messages.error(request,"No disponemos de la cantidad solicitada. Stock actual: " + str(item_venta.item.cantidad))
        return item_venta.item.nombre + " (No disponemos de la cantidad solicitada. Stock actual: " + str(item_venta.item.cantidad) + ")"
    
    
    if item_venta.cantidad_solicitada < 0:
        #messages.error(request,"La cantidad no puede ser negativa.") 
        return item_venta.item.nombre + " (La cantidad no puede ser negativa)"
    
    if item_venta.cantidad_solicitada == 0:
        return item_venta.item.nombre + " (Debe seleccionar una cantidad)"


def CambiarEstado(request, id):

    queryset = Venta.objects.filter(numero_comprobante = id)

    ids = EstadoVenta.objects.filter(opciones = 'LISTA')
    nuevo_estado = ""
    instancia = None

    for id in ids:
        nuevo_estado = id.id

    for venta in queryset:
        instancia = venta
        
        if instancia.total >= 10000 and instancia.cliente_asociado.nombre == 'CONSUMIDOR FINAL':
            messages.error(request, "Es necesario registrar al cliente para agregar el item")
            return redirect('ventas:listar_ventas')
        # if instancia.vendedor_asociado.id != request.user.id:
        #     messages.error(request, "No puedes cargar una venta de otra sucursal.")
        #     return redirect('ventas:listar_ventas')
        if instancia.total == 0:
            messages.error(request, 'No puedes cargar una venta sin items.')
            return redirect('ventas:listar_ventas')
        venta.estado_id = nuevo_estado
        venta.save()

    messages.success(request, "Venta lista para su ejecucion.")
    return redirect('ventas:listar_ventas')


def eliminarItem(request, venta, item):
    
    item_venta = ItemVenta.objects.filter(venta_asociada = venta, id = item)
    
    item_asociado = 0
    venta_asociada = 0
    cantidad_solicitada = 0
    monto = 0
    
    for item in item_venta:
        item_asociado = item.item_id 
        venta_asociada = item.venta_asociada_id   
        cantidad_solicitada = item.cantidad_solicitada
        monto = item.monto
        
    
    item_de_venta = Item.objects.filter(id = item_asociado)  
   
    for item in item_de_venta:
        
        item.cantidad += cantidad_solicitada
        item.save() 
        
    queryset = Venta.objects.filter(numero_comprobante = venta_asociada)
    
    for venta in queryset:
        
        venta.total -= monto
        venta.save()
        
    item_venta.delete()
    
    messages.error(request, "Se ha quitado el item de la venta.")
    return redirect('ventas:listar_ventas')

def eliminarItemCajero(request, venta, item):
    
    item_venta = ItemVenta.objects.filter(venta_asociada = venta, id = item)
    
    item_asociado = 0
    venta_asociada = 0
    cantidad_solicitada = 0
    monto = 0
    
    for item in item_venta:
        item_asociado = item.item_id 
        venta_asociada = item.venta_asociada_id   
        cantidad_solicitada = item.cantidad_solicitada
        monto = item.monto
        
    
    item_de_venta = Item.objects.filter(id = item_asociado)  
   
    for item in item_de_venta:
        
        item.cantidad += cantidad_solicitada
        item.save() 
        
    queryset = Venta.objects.filter(numero_comprobante = venta_asociada)
    
    for venta in queryset:
        
        venta.total -= monto
        venta.save()
        
    item_venta.delete()
    
    messages.error(request, "Se ha quitado el item de la venta.")
    return redirect('ventas:listar_ventas_cajero')

def FinalizarVenta(request, venta):
    
    venta_obtenida = Venta.objects.filter(numero_comprobante = venta)
    instancia = None
    sucursal_asociada = 0
    total = 0
  
    for venta in venta_obtenida:
        
        instancia = venta
        sucursal_asociada = venta.sucursal_asociada
        total += venta.total
        
    cajas = Caja.objects.filter(sucursal_id = sucursal_asociada.id)
    
    if instancia.total <= 0:
        messages.error(request, "No es posible realizar una venta sin agregar items.")
        return redirect('ventas:listar_ventas_cajero')
    
    
    caja_menor = None
    monto = total
    
    for caja in cajas:
        
        if caja.saldo_disponible < monto:
            monto = caja.saldo_disponible
            caja_menor = caja
        else:
            caja_menor = caja
    
    caja_menor.saldo_disponible = caja_menor.saldo_disponible + total
    caja_menor.save()
    ids = EstadoVenta.objects.filter(opciones = 'PAGADA')
    nuevo_estado = ""
    for id in ids:
        nuevo_estado = id.id
        
    instancia.estado_id = nuevo_estado
    instancia.save()
    movimiento = Operacion()
    movimiento.monto = "+" + str(total) 
    movimiento.tipo = "Venta"
    movimiento.caja_asociada = caja_menor
    movimiento.identificador = "Número de comprobante" + str(instancia.numero_comprobante)
    movimiento.save()
    
    messages.success(request, "Venta finalizada con éxito.")  
    
    return redirect('ventas:listar_ventas_cajero')