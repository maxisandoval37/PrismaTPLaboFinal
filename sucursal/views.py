from django.shortcuts import render, redirect
from django.views.generic import CreateView,DeleteView,ListView,UpdateView, DetailView
from django.urls import reverse_lazy
from .forms import SucursalForm, CajaForm
from .models import Sucursal, Caja
from usuario.mixins import ValidarLoginYPermisosRequeridos
from item.models import Item


class ListarSucursal(ValidarLoginYPermisosRequeridos,ListView):
    model = Sucursal
    template_name = 'sucursales/listar_sucursal.html'

class RegistrarSucursal(ValidarLoginYPermisosRequeridos,CreateView):
    model = Sucursal
    form_class = SucursalForm
    template_name = 'sucursales/crear_sucursal.html'
    success_url = reverse_lazy('sucursales:listar_sucursales')


class EliminarSucursal(ValidarLoginYPermisosRequeridos,DeleteView):
    model = Sucursal
    template_name = 'sucursales/eliminar.html'
    success_url = reverse_lazy('sucursales:listar_sucursales')
    
class RegistrarCaja(ValidarLoginYPermisosRequeridos,CreateView):
    
    model = Caja
    form_class = CajaForm
    template_name = 'sucursales/crear_caja.html'
    success_url = reverse_lazy('sucursales:listar_sucursales')




def idCaja(request, id):
    
    caja = Caja.objects.get(id = id)
    queryset = Caja.objects.filter(id = caja.id)
    lista = []
    for caja in queryset:
        dic = {
            "saldo_disponible": caja.saldo_disponible,
            "egresos": caja.egresos,
            "ingresos": caja.ingresos,
            "saldo_inicial": caja.saldo_inicial,
            "saldo_final": caja.saldo_final,
            
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
    
    sucursales = Sucursal.objects.all()
    lista = []
    egresosTotal = 0
    ingresosTotal = 0
    
    for sucursal in sucursales:
    
        egresosTotal += sucursal.caja.egresos
        ingresosTotal += sucursal.caja.ingresos
        
    dic = {
        "egresos": egresosTotal,
        "ingresos": ingresosTotal,
    }
    lista.append(dic)
    
    return render(request, 'sucursales/consolidado.html', locals())