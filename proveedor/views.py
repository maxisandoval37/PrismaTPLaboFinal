from django.shortcuts import render
from .forms import ProveedorForm
from .models import Proveedor
from django.views.generic import  CreateView, UpdateView, DeleteView, ListView
from usuario.mixins import ValidarLoginYPermisosRequeridos
from django.urls import reverse_lazy



class ListadoProveedor(ValidarLoginYPermisosRequeridos,ListView):
    
    model = Proveedor
    template_name = 'proveedores/listar_proveedor.html'



class RegistrarProveedor(ValidarLoginYPermisosRequeridos,CreateView):
    
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'proveedores/crear_proveedor.html'
    success_url = reverse_lazy('proveedores:listar_proveedores')
    
class EditarProveedor(ValidarLoginYPermisosRequeridos,UpdateView):
    
    model = Proveedor
    fields = ['email','telefono','calle','numero','localidad','cod_postal']
    template_name = 'proveedores/crear_proveedor.html'
    success_url = reverse_lazy('proveedores:listar_proveedores')
    
class EliminarProveedor(ValidarLoginYPermisosRequeridos,DeleteView):
    
    model = Proveedor
    template_name = 'proveedores/eliminar_proveedor.html'
    success_url = reverse_lazy('proveedores:listar_proveedores')
                                    
                                    