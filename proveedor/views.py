from django.shortcuts import render, HttpResponseRedirect, redirect
from .forms import ProveedorForm, CuentaCorrienteProveedorForm
from .models import Proveedor, CuentaCorrienteProveedor
from django.views.generic import  CreateView, UpdateView, DeleteView, ListView
from usuario.mixins import ValidarLoginYPermisosRequeridos
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.db.models import ProtectedError
from django.contrib.messages.views import SuccessMessageMixin


class ListadoProveedor(ValidarLoginYPermisosRequeridos,ListView):
    
    permission_required = ('proveedor.view_proveedor',)
    model = Proveedor
    template_name = 'proveedores/listar_proveedor.html'



class RegistrarProveedor(ValidarLoginYPermisosRequeridos,SuccessMessageMixin,CreateView):
    
    permission_required = ('proveedor.view_proveedor','proveedor.add_proveedor','proveedor.change_proveedor','proveedor.delete_proveedor',)
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'proveedores/crear_proveedor.html'
    success_url = reverse_lazy('proveedores:listar_proveedores')
    success_message = 'Proveedor registrado correctamente.'
    
    
class EditarProveedor(ValidarLoginYPermisosRequeridos,SuccessMessageMixin,UpdateView):
    
    permission_required = ('proveedor.view_proveedor','proveedor.add_proveedor','proveedor.change_proveedor','proveedor.delete_proveedor',)
    model = Proveedor
    fields = ['email','telefono','calle','numero','localidad','cod_postal']
    template_name = 'proveedores/crear_proveedor.html'
    success_url = reverse_lazy('proveedores:listar_proveedores')
    success_message = 'Se editó el proveedor correctamente.'
    
class EliminarProveedor(ValidarLoginYPermisosRequeridos,SuccessMessageMixin,DeleteView):
    
    permission_required = ('proveedor.view_proveedor','proveedor.add_proveedor','proveedor.change_proveedor','proveedor.delete_proveedor',)
    model = Proveedor
    template_name = 'proveedores/eliminar_proveedor.html'
    success_url = reverse_lazy('proveedores:listar_proveedores')
    success_message = 'Se eliminó el proveedor correctamente.'
                                    
    def delete(self, request, *args, **kwargs):
        
        self.object = self.get_object()
        success_url = self.get_success_url()

        try:
            self.object.delete()
        except ProtectedError:
            messages.add_message(request, messages.ERROR, 'No se puede eliminar: Este proveedor esta relacionado.')
            return redirect('proveedores:listar_proveedores')

        return HttpResponseRedirect(success_url)                                
    
class RegistrarCuentaCorrienteProveedor(ValidarLoginYPermisosRequeridos,SuccessMessageMixin,CreateView):
    
    permission_required = ('proveedor.view_proveedor','proveedor.add_proveedor','proveedor.change_proveedor','proveedor.delete_proveedor',)
    model = CuentaCorrienteProveedor
    form_class = CuentaCorrienteProveedorForm
    success_message = 'Se registró la cuenta corriente.'
    template_name = 'proveedores/crear_cuenta_corriente.html'
    success_url = reverse_lazy('proveedores:listar_proveedores')