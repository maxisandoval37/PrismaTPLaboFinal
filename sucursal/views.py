from django.shortcuts import render, redirect
from django.views.generic import CreateView,DeleteView,ListView,UpdateView, DetailView
from django.urls import reverse_lazy
from .forms import SucursalForm
from .models import Sucursal 
from usuario.mixins import ValidarLoginYPermisosRequeridos
from item.models import Item
from django.http import HttpResponseRedirect

class ListarSucursal(ValidarLoginYPermisosRequeridos,ListView):
    model = Sucursal
    template_name = 'sucursales/listar_sucursal.html'

class RegistrarSucursal(ValidarLoginYPermisosRequeridos,CreateView):
    model = Sucursal
    form_class = SucursalForm
    template_name = 'sucursales/crear_sucursal.html'
    success_url = reverse_lazy('sucursales:listar_sucursales')

class EditarSucursal(ValidarLoginYPermisosRequeridos,UpdateView):
    model = Sucursal
    fields = ['nombre','direccion']
    template_name = 'sucursales/crear_sucursal.html'
    success_url = reverse_lazy('sucursales:listar_sucursales')

class EliminarSucursal(ValidarLoginYPermisosRequeridos,DeleteView):
    model = Sucursal
    template_name = 'sucursales/eliminar.html'
    success_url = reverse_lazy('sucursales:listar_sucursales')
    
class VisualizarItems(ValidarLoginYPermisosRequeridos,ListView):
    
    model = Item
    template_name = 'sucursales/visualizar_items.html'
    queryset = Item.objects.prefetch_related('sucursal')
    
    
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
   
    print(lista)
    return render(request, 'sucursales/visualizar_items.html',locals())
    
