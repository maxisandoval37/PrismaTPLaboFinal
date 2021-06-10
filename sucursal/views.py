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
    queryset = Sucursal.objects.all().order_by('id')

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
            "caja_codigo": caja.codigo,
            "saldo_disponible": caja.saldo_disponible,
            "saldo_disponible_dolares": caja.saldo_disponible_dolares,
            "saldo_disponible_euros": caja.saldo_disponible_euros,
            "ingresos_en_pesos": caja.ingresos_en_pesos,
            "ingresos_en_dolares": caja.ingresos_en_dolares,
            "ingresos_en_euros": caja.ingresos_en_euros,
            "egresos": caja.egresos,
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
    ingresos_en_pesos = 0
    ingresos_en_dolares = 0
    ingresos_en_euros = 0
    lista = []
    for caja in cajas:
        
        egresosTotal += caja.egresos
        ingresos_en_pesos += caja.ingresos_en_pesos
        ingresos_en_dolares += caja.ingresos_en_dolares 
        ingresos_en_euros += caja.ingresos_en_euros
        
        
    dic = {
        "egresos": egresosTotal,
        "ingresos_en_pesos": ingresos_en_pesos,
        "ingresos_en_dolares": ingresos_en_dolares,
        "ingresos_en_euros": ingresos_en_euros,
    }
    lista.append(dic)
    
    return render(request, 'sucursales/consolidado.html', locals())

def consolidacionPorSucursal(request, id):
    
    sucursal = Sucursal.objects.get(id = id)
    cajas = Caja.objects.filter(sucursal_id = sucursal.id)
    egresosTotal = 0
    ingresos_en_pesos = 0
    ingresos_en_dolares = 0
    ingresos_en_euros = 0
    lista = []
    for caja in cajas:
        
        egresosTotal += caja.egresos
        ingresos_en_pesos += caja.ingresos_en_pesos
        ingresos_en_dolares += caja.ingresos_en_dolares 
        ingresos_en_euros += caja.ingresos_en_euros
        
        
    dic = {
        "egresos": egresosTotal,
        "ingresos_en_pesos": ingresos_en_pesos,
        "ingresos_en_dolares": ingresos_en_dolares,
        "ingresos_en_euros": ingresos_en_euros,
    }
    lista.append(dic)
    
    return render(request, 'sucursales/consolidadoSucursal.html', locals())