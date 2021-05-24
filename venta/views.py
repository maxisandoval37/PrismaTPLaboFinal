from django.shortcuts import render, HttpResponseRedirect, redirect
from .forms import VentaLocalForm, VentaVirtualForm, ItemVentaForm
from .models import EstadoVenta, VentaLocal, VentaVirtual, Venta, ItemVenta
from django.views.generic import  CreateView,  DeleteView, ListView
from usuario.mixins import ValidarLoginYPermisosRequeridos
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import ProtectedError
from cliente.models import Cliente, CuentaCorriente,MedioDePago
from sucursal.models import Sucursal, Caja
from usuario.models import Vendedor
from item.models import Item
from django.http import HttpResponse, HttpResponseBadRequest
from decimal import Decimal
from django.core.exceptions import ValidationError


class ListadoVenta(ValidarLoginYPermisosRequeridos,ListView):
    
    permission_required = ('venta.view_venta',)
    model = Venta
    template_name = 'ventas/listar_venta.html'

class ListadoVentaCajero(ValidarLoginYPermisosRequeridos,ListView):
    
    permission_required = ('venta.view_venta',)
    model = Venta 
    template_name = 'ventas/listar_venta_cajero.html'


class RegistrarVentaLocal(ValidarLoginYPermisosRequeridos,CreateView):
    
    permission_required = ('venta.view_venta','venta.add_venta',)
    model = VentaLocal
    context_object_name = 'obj'
    form_class = VentaLocalForm
    template_name = 'ventas/crear_venta_local.html'
    success_url = reverse_lazy('ventas:listar_ventas')
      
    
    def get_context_data(self, **kwargs):
        context = super(RegistrarVentaLocal, self).get_context_data(**kwargs)
        context["cliente_asociado"] = Cliente.objects.all()
        context["mediodepago"] = MedioDePago.objects.all()
        context["cuenta_corriente"] = CuentaCorriente.objects.all()
        context["sucursal_asociada"] = Sucursal.objects.all()
        context["vendedor_asociado"] = Vendedor.objects.all()
        return context
    
    
    
    
class RegistrarVentaVirtual(ValidarLoginYPermisosRequeridos,CreateView):
    
    permission_required = ('venta.view_venta','venta.add_venta',)
    model = VentaVirtual
    context_object_name = 'obj'
    form_class = VentaVirtualForm
    template_name = 'ventas/crear_venta_virtual.html'
    success_url = reverse_lazy('ventas:listar_ventas')
    
    def get_context_data(self, **kwargs):
        context = super(RegistrarVentaVirtual, self).get_context_data(**kwargs)
        context["cliente_asociado"] = Cliente.objects.all()
        context["mediodepago"] = MedioDePago.objects.all()
        context["cuenta_corriente"] = CuentaCorriente.objects.all()
        context["sucursal_asociada"] = Sucursal.objects.all()
        context["vendedor_asociado"] = Vendedor.objects.all()
        return context
    
class EliminarVenta(ValidarLoginYPermisosRequeridos,DeleteView):
    
    permission_required = ('venta.view_venta','venta.delete_venta',)
    model = Venta
    template_name = 'ventas/eliminar_venta.html'
    success_url = reverse_lazy('ventas:listar_ventas')
                                    
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
    queryset = Item.objects.filter(sucursal = sucursal.id, estado = 1)
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
        item = request.POST.get('item', None)
        cantidad = request.POST.get('cantidad', None)
        sucursal = request.POST.get('sucursal', None)
        venta = request.POST.get('venta', None)
        precio = request.POST.get('precio', None)
        
        if cantidad == '':
            return HttpResponseBadRequest()
        
        item_venta = ItemVenta()
        item_venta.item_id = int(item)
        item_venta.cantidad_solicitada = int(cantidad)
        item_venta.sucursal_asociada_id = str(sucursal)
        item_venta.venta_asociada_id = int(venta)
        item_venta.monto = Decimal(cantidad.replace(',', '.')) * Decimal(precio.replace(',', '.'))
        
       
         
        if item_venta.item.cantidad == 0:
            #messages.error(request, "No hay stock del item solicitado.")
            return HttpResponseBadRequest() 
        
        if item_venta.item.precio != item_venta.monto:
            #messages.error(request,"El precio del item es: "+str(item_venta.item.precio))
            return HttpResponseBadRequest() 
        # if item_venta.item.precio >= 10000:
        #     raise ValidationError("El cliente debe ser registrado para finalizar la venta.")
        
        if item_venta.item.cantidad < item_venta.cantidad_solicitada:
            #messages.error(request,"No disponemos de la cantidad solicitada. Stock actual: " + str(item_venta.item.cantidad))
            return HttpResponseBadRequest() 
              
        # if item_venta.monto <= 0:
        #     messages.error(request,"Debe ingresar un monto valido.")
        #     return HttpResponseBadRequest() 
       
        
        if item_venta.cantidad_solicitada < 0:
           # messages.error(request,"La cantidad no puede ser negativa.") 
            return HttpResponseBadRequest() 
       
        if item_venta.cantidad_solicitada == None or item_venta.cantidad_solicitada <= 0:
           # messages.error(request,"Debe ingresar una cantidad para solicitar.")
            return HttpResponseBadRequest() 
        
        item_venta.save()
        
        item_de_venta = Item.objects.filter(id = item_venta.item_id)  
        
        for item in item_de_venta:
            
            item.cantidad -= item_venta.cantidad_solicitada
            item.save() 
            
        queryset = Venta.objects.filter(id = item_venta.venta_asociada_id)
        
        for venta in queryset:
           
            venta.total += item_venta.monto
            
            venta.save()
            
        messages.success(request, "Item agregado correctamente.")
        return HttpResponse()
    

def CambiarEstado(request, id):
    
    queryset = Venta.objects.filter(id = id)
    
    
    for venta in queryset:
       
        venta.estado = EstadoVenta(2)
        
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
        
    queryset = Venta.objects.filter(id = venta_asociada)
    
    for venta in queryset:
        
        venta.total -= monto
        venta.save()
        
    item_venta.delete()
    
    messages.error(request, "Se ha quitado el item de la venta.")
    return redirect('ventas:listar_ventas')


def FinalizarVenta(request, venta):
    
    venta_obtenida = Venta.objects.filter(id = venta)
    instancia = None
    sucursal_asociada = 0
    total = 0
  
    for venta in venta_obtenida:
        
        instancia = venta
        sucursal_asociada = venta.sucursal_asociada
        total = venta.total
        
    cajas = Caja.objects.filter(sucursal_id = sucursal_asociada)
        
    for caja in cajas:   
        if caja.saldo_disponible < total:
            messages.error(request, "Saldo insuficiente en las cajas de la sucursal.")
            return redirect('ventas:listar_ventas_cajero')
        
        else:
            caja.saldo_disponible = caja.saldo_disponible - total
            caja.save()
            instancia.estado = EstadoVenta(3)
            instancia.save()
            messages.success(request, "Venta finalizada con éxito.")  
            return redirect('ventas:listar_ventas_cajero')