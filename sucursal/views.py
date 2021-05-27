from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views.generic import CreateView,DeleteView,ListView,UpdateView, DetailView
from django.urls import reverse_lazy
from .forms import SucursalForm, CajaForm
from .models import Sucursal, Caja
from usuario.mixins import ValidarLoginYPermisosRequeridos
from item.models import Item
from django.contrib import messages
from django.db.models import ProtectedError
from django.contrib.messages.views import SuccessMessageMixin

class ListarSucursal(ValidarLoginYPermisosRequeridos,ListView):
    
    permission_required = ('sucursal.view_sucursal',)
    model = Sucursal
    template_name = 'sucursales/listar_sucursal.html'

class RegistrarSucursal(ValidarLoginYPermisosRequeridos,SuccessMessageMixin,CreateView):
    
    permission_required = ('sucursal.view_sucursal','sucursal.add_sucursal',)
    model = Sucursal
    form_class = SucursalForm
    template_name = 'sucursales/crear_sucursal.html'
    success_url = reverse_lazy('sucursales:listar_sucursales')
    success_message = 'Sucursal registrada correctamente.'


class EliminarSucursal(ValidarLoginYPermisosRequeridos,SuccessMessageMixin,DeleteView):
    
    permission_required = ('sucursal.view_sucursal','sucursal.delete_sucursal',)
    model = Sucursal
    template_name = 'sucursales/eliminar.html'
    success_url = reverse_lazy('sucursales:listar_sucursales')
    success_message = 'Se eliminó la sucursal correctamente.'
    
    def delete(self, request, *args, **kwargs):
        
        self.object = self.get_object()
        success_url = self.get_success_url()

        try:
            self.object.delete()
        except ProtectedError:
            messages.add_message(request, messages.ERROR, 'No se puede eliminar: Esta sucursal esta relacionada.')
            return redirect('items:listar_items')

        return HttpResponseRedirect(success_url)
    
    
class RegistrarCaja(ValidarLoginYPermisosRequeridos,SuccessMessageMixin,CreateView):
    
    permission_required = ('sucursal.view_caja','sucursal.add_caja',)
    model = Caja
    form_class = CajaForm
    template_name = 'sucursales/crear_caja.html'
    success_url = reverse_lazy('sucursales:listar_sucursales')
    success_message = 'Caja registrada correctamente.'



def idCaja(request, id):
    
    sucursal = Sucursal.objects.get(id = id)
    queryset = Caja.objects.filter(sucursal_id = sucursal.id)
    lista = []
    for caja in queryset:
        dic = {
            "saldo_disponible": caja.saldo_disponible,
            "egresos": caja.egresos,
            "ingresos": caja.ingresos,
            "saldo_inicial": caja.saldo_inicial,
            "saldo_final": caja.saldo_final,
            "sucursal_id": caja.sucursal_id,
            
        }
        lista.append(dic) 
   
    
    return render(request, 'sucursales/visualizar_cajas.html',locals())
    

    
    
def idSucursal(request, id):
    
    sucursal = Sucursal.objects.get(id = id)
    queryset = Item.objects.filter(sucursal = sucursal.id)
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
        }
        lista.append(dic) 
   
    
    return render(request, 'sucursales/visualizar_items.html',locals())
    

def consolidacionSucursales(request):
    
    cajas = Caja.objects.all()
    lista = []
    egresosTotal = 0
    ingresosTotal = 0
    
    for caja in cajas:
    
        egresosTotal += caja.egresos
        ingresosTotal += caja.ingresos
        
    dic = {
        "egresos": egresosTotal,
        "ingresos": ingresosTotal,
    }
    lista.append(dic)
    
    return render(request, 'sucursales/consolidado.html', locals())

def consolidacionPorSucursal(request, id):
    
    sucursal = Sucursal.objects.get(id = id)
    cajas = Caja.objects.filter(sucursal_id = sucursal.id)
    egresosTotal = 0
    ingresosTotal = 0
    lista = []
    for caja in cajas:
        
        egresosTotal += caja.egresos
        ingresosTotal += caja.ingresos
        
    dic = {
        "egresos": egresosTotal,
        "ingresos": ingresosTotal,
    }
    lista.append(dic)
    
    return render(request, 'sucursales/consolidadoSucursal.html', locals())