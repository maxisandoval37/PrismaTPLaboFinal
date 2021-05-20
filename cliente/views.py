from django.shortcuts import render, HttpResponseRedirect, redirect
from .forms import ClienteForm
from .models import Cliente
from django.views.generic import  CreateView, UpdateView, DeleteView, ListView
from usuario.mixins import ValidarLoginYPermisosRequeridos
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import ProtectedError



class ListadoCliente(ValidarLoginYPermisosRequeridos,ListView):
    
    model = Cliente
    template_name = 'clientes/listar_cliente.html'



class RegistrarCliente(ValidarLoginYPermisosRequeridos,CreateView):
    
    model = Cliente
    form_class = ClienteForm
    template_name = 'clientes/crear_cliente.html'
    success_url = reverse_lazy('clientes:listar_clientes')
   
    
    
class EditarCliente(ValidarLoginYPermisosRequeridos,UpdateView):
    
    model = Cliente
    fields = ['email','telefono','categoria_cliente','estado_cliente','estado_deuda']
    template_name = 'clientes/crear_cliente.html'
    success_url = reverse_lazy('clientes:listar_clientes')
 
    
class EliminarCliente(ValidarLoginYPermisosRequeridos,DeleteView):
    
    model = Cliente
    template_name = 'clientes/eliminar_proveedor.html'
    success_url = reverse_lazy('proveedores:listar_clientes')
                                    
    def delete(self, request, *args, **kwargs):
        
        self.object = self.get_object()
        success_url = self.get_success_url()

        try:
            self.object.delete()
        except ProtectedError:
            messages.add_message(request, messages.ERROR, 'No se puede eliminar: Este Cliente esta relacionado.')
            return redirect('clientes:listar_clientes')

        return HttpResponseRedirect(success_url)  
