from django.shortcuts import render, HttpResponseRedirect, redirect
from .forms import PresupuestoForm
from .models import EstadoPresupuesto, Presupuesto
from django.views.generic import  CreateView, UpdateView, DeleteView, ListView
from usuario.mixins import ValidarLoginYPermisosRequeridos
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import ProtectedError
from sucursal.models import Sucursal
from usuario.models import Vendedor
from presupuesto.models import ItemPresupuesto
from django.http import HttpResponse, HttpResponseBadRequest
from decimal import Decimal
import json
from item.models import Item, Estado
from django.contrib.messages.views import SuccessMessageMixin



class ListadoPresupuesto(ValidarLoginYPermisosRequeridos,ListView):
    
    permission_required = ('presupuesto.view_presupuesto',)
    model = Presupuesto
    template_name = 'presupuestos/listar_presupuesto.html'
    queryset = Presupuesto.objects.all().order_by('id')


class RegistrarPresupuesto(ValidarLoginYPermisosRequeridos,SuccessMessageMixin,CreateView):
    
    permission_required = ('presupuesto.view_presupuesto','presupuesto.add_presupuesto',)
    model = Presupuesto
    form_class = PresupuestoForm
    success_message = 'Presupuesto registrado correctamente.'
    template_name = 'presupuestos/crear_presupuesto.html'
    success_url = reverse_lazy('presupuestos:listar_presupuestos')
    
    def get_context_data(self, **kwargs):
        context = super(RegistrarPresupuesto, self).get_context_data(**kwargs)
        context["sucursal_asociada"] = Sucursal.objects.all()
        context["vendedor_asociado"] = Vendedor.objects.all()
        return context
    
class EliminarPresupuesto(ValidarLoginYPermisosRequeridos,SuccessMessageMixin,DeleteView):
    
    permission_required = ('presupuesto.view_presupuesto','presupuesto.delete_presupuesto',)
    model = Presupuesto
    template_name = 'presupuestos/eliminar_presupuesto.html'
    success_message = 'Presupuesto eliminado correctamente.'
    success_url = reverse_lazy('presupuestos:listar_presupuestos')
                                    
    def delete(self, request, *args, **kwargs):
        
        self.object = self.get_object()
        success_url = self.get_success_url()

        try:
            self.object.delete()
        except ProtectedError:
            messages.add_message(request, messages.ERROR, 'No se puede eliminar: Este presupuesto esta relacionado.')
            return redirect('presupuestos:listar_presupuestos')

        return HttpResponseRedirect(success_url)                                
    
    
def ListarItem(request, presupuesto):
    
    
    items = ItemPresupuesto.objects.filter(presupuesto_asociado = presupuesto)
   
    lista = []
    for item in items:
        
        lista.append(item)
   
    return render(request, 'presupuestos/listar_itempresupuesto.html', locals())

        
        
def VerDetalle(request, sucursal, presupuesto):
    
   
    sucursal = Sucursal.objects.get(id = sucursal)
    estado_activo = ""
    ids = Estado.objects.filter(opciones = 'ACTIVO')
    for id in ids:
        estado_activo = id
    
    queryset = Item.objects.filter(sucursal = sucursal.id, estado = estado_activo)
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
            "presupuesto": presupuesto,
            
        }
        lista.append(dic)
         
   
    
    return render(request, 'presupuestos/crear_itempresupuesto.html',locals())


def AgregarItem(request, sucursal, presupuesto):
    
    
    if request.is_ajax():
        object = json.loads(request.POST.get('items'))
        
        lista_items = []
        lista_presupuestos = []
        lista_errores = []
        lista_success = []
        
        for info in object:
            objeto = json.loads(info)
            
            item = objeto['item']
            cantidad = objeto['cantidad']
            sucursal = objeto['sucursal']
            presupuesto = objeto['presupuesto']
            precio = objeto['precio']
            
            item_presupuesto = ItemPresupuesto()
            item_presupuesto.item_id = int(item)
            item_presupuesto.cantidad_solicitada = int(cantidad)
            item_presupuesto.sucursal_asociada_id = str(sucursal)
            item_presupuesto.presupuesto_asociado_id = int(presupuesto)
            item_presupuesto.monto = Decimal(cantidad.replace(',', '.')) * Decimal(precio.replace(',', '.'))
            
            
            
            validacion = validar(request, item_presupuesto)
            
            if validacion != None:
                lista_errores.append(validacion)
                continue
            else:
                lista_success.append(item_presupuesto.item.nombre)
                
            lista_items.append(item_presupuesto.item_id)
            lista_presupuestos.append(item_presupuesto.presupuesto_asociado_id)
            
            item_presupuesto.save()
            
            queryset = Presupuesto.objects.raw("""
                SELECT * 
                FROM presupuesto_presupuesto
                WHERE id IN %s               
            """, [tuple(lista_presupuestos)])  
            
        
            for presupuesto in queryset:
                
                presupuesto.total += item_presupuesto.monto
               
                presupuesto.save()
        
        
            
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
    

def validar(request, item_presupuesto):
    
    if item_presupuesto.item.cantidad == 0:
           
            return item_presupuesto.item.nombre
        
    
    if item_presupuesto.item.cantidad < item_presupuesto.cantidad_solicitada:
        messages.error(request,"No disponemos de la cantidad solicitada. Stock actual: " + str(item_presupuesto.item.cantidad))
        return item_presupuesto.item.nombre 
    
    
    if item_presupuesto.cantidad_solicitada < 0:
        
        return item_presupuesto.item.nombre 
    
    if item_presupuesto.cantidad_solicitada == None or item_presupuesto.cantidad_solicitada == 0:
        
        return item_presupuesto.item.nombre 
        



def AprobarPresupuesto(request, id):
    
    queryset = Presupuesto.objects.filter(id = id)
    
    ids = EstadoPresupuesto.objects.filter(opciones = 'APROBADO')
    nuevo_estado = ""
    for id in ids:
        nuevo_estado = id.id
              
    for presupuesto in queryset:
        
        if presupuesto.total == 0:
            messages.error(request, 'No puedes aprobar un presupuesto sin items.')
            return redirect('presupuestos:listar_presupuestos')
        presupuesto.estado_id = nuevo_estado
        presupuesto.save()
       
    messages.success(request, "Presupuesto aprobado.")
    
    return redirect('presupuestos:listar_presupuestos')

def RechazarPresupuesto(request, id):
    
    queryset = Presupuesto.objects.filter(id = id)
    
    ids = EstadoPresupuesto.objects.filter(opciones = 'RECHAZADO')
    nuevo_estado = ""
    for id in ids:
        nuevo_estado = id.id
              
    for presupuesto in queryset:
       
        presupuesto.estado_id = nuevo_estado
        presupuesto.save()
       
    messages.success(request, "Presupuesto rechazado.")
    
    return redirect('presupuestos:listar_presupuestos')


def eliminarItem(request, presupuesto, item):
    
    item_presupuesto = ItemPresupuesto.objects.filter(presupuesto_asociado = presupuesto, id = item)
    
    presupuesto_asociado = 0
    monto = 0
    
    for item in item_presupuesto:
       
        presupuesto_asociado = item.presupuesto_asociado_id   
        monto = item.monto
        
   
        
    queryset = Presupuesto.objects.filter(id = presupuesto_asociado)
    
    for presupuesto in queryset:
        
        presupuesto.total -= monto
        presupuesto.save()
        
    item_presupuesto.delete()
    
    messages.error(request, "Se ha quitado el item del presupuesto.")
    return redirect('presupuestos:listar_presupuestos')