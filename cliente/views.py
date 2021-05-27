from django.shortcuts import render, HttpResponseRedirect, redirect
from .forms import ClienteForm, CuentaCorrienteForm, MedioDePagoForm
from .models import Cliente, CuentaCorriente, MedioDePago
from django.views.generic import  CreateView, UpdateView, DeleteView, ListView
from usuario.mixins import ValidarLoginYPermisosRequeridos
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin



class ListadoCliente(ValidarLoginYPermisosRequeridos,ListView):
    
    permission_required = ('cliente.view_cliente',)
    model = Cliente
    template_name = 'clientes/listar_cliente.html'



class RegistrarCliente(ValidarLoginYPermisosRequeridos,SuccessMessageMixin,CreateView):
    
    permission_required = ('cliente.view_cliente','cliente.add_cliente',)
    model = Cliente
    form_class = ClienteForm
    template_name = 'clientes/crear_cliente.html'
    success_url = reverse_lazy('clientes:listar_clientes')
    success_message = "Cliente registrado con exito."
    
    
class EditarCliente(ValidarLoginYPermisosRequeridos,SuccessMessageMixin,UpdateView):
    
    permission_required = ('cliente.view_cliente','cliente.change_cliente',)
    model = Cliente
    fields = ['email','telefono','categoria_cliente','estado_cliente']
    success_message = 'Se editó al cliente correctamente.'
    template_name = 'clientes/crear_cliente.html'
    success_url = reverse_lazy('clientes:listar_clientes')
 
    
# class EliminarCliente(ValidarLoginYPermisosRequeridos,DeleteView):
    
#     permission_required = ('cliente.view_cliente','cliente.add_cliente',)
#     model = Cliente
#     template_name = 'clientes/eliminar_proveedor.html'
#     success_url = reverse_lazy('proveedores:listar_clientes')
                                    
#     def delete(self, request, *args, **kwargs):
        
#         self.object = self.get_object()
#         success_url = self.get_success_url()

#         try:
#             self.object.delete()
#         except ProtectedError:
#             messages.add_message(request, messages.ERROR, 'No se puede eliminar: Este Cliente esta relacionado.')
#             return redirect('clientes:listar_clientes')

#         return HttpResponseRedirect(success_url)  


class RegistrarMDP(ValidarLoginYPermisosRequeridos,SuccessMessageMixin,CreateView):
    permission_required = ('cliente.view_mediodepago','cliente.add_mediodepago',)
    model = MedioDePago
    form_class = MedioDePagoForm
    success_message = 'Se registró el medio de pago.'
    template_name = 'ventas/crear_mdp.html'
    
    
    def get_success_url(self):
        return self.request.GET.get('next', reverse('ventas:registrar_venta_local'))
    
class RegistrarCuentaCorriente(ValidarLoginYPermisosRequeridos,SuccessMessageMixin,CreateView):
    
    permission_required = ('cliente.view_cuentacorriente','cliente.add_cuentacorriente',)
    model = CuentaCorriente
    form_class = CuentaCorrienteForm
    success_message = 'Se registró la cuenta corriente.'
    template_name = 'clientes/crear_cuenta_corriente.html'
    def get_success_url(self):
        return self.request.GET.get('next', reverse('ventas:registrar_venta_local'))