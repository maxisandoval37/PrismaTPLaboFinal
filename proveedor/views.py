from django.shortcuts import render, HttpResponseRedirect, redirect
from .forms import ProveedorForm, CuentaCorrienteProveedorForm
from .models import Proveedor, CuentaCorrienteProveedor
from django.views.generic import  CreateView, UpdateView, DeleteView, ListView
from usuario.mixins import ValidarLoginYPermisosRequeridos
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import ProtectedError
from django.contrib.messages.views import SuccessMessageMixin
from item.models import Pedidos


class ListadoProveedor(ValidarLoginYPermisosRequeridos,ListView):
    
    permission_required = ('proveedor.view_proveedor',)
    model = Proveedor
    template_name = 'proveedores/listar_proveedor.html'
    queryset = Proveedor.objects.all().order_by('id')

class ListadoCuentasCorriente(ValidarLoginYPermisosRequeridos, ListView):
    
    permission_required = ('proveedor.view_cuentacorrienteproveedor',)
    model = CuentaCorrienteProveedor
    template_name = 'proveedores/listar_cuenta_corriente.html'
    queryset = CuentaCorrienteProveedor.objects.all().order_by('numero_cuenta')

class RegistrarProveedor(ValidarLoginYPermisosRequeridos,SuccessMessageMixin,CreateView):
    
    permission_required = ('proveedor.view_proveedor','proveedor.add_proveedor',)
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'proveedores/crear_proveedor.html'
    success_url = reverse_lazy('proveedores:listar_proveedores')
    success_message = 'Proveedor registrado correctamente.'
    
    
class EditarProveedor(ValidarLoginYPermisosRequeridos,SuccessMessageMixin,UpdateView):
    
    permission_required = ('proveedor.view_proveedor','proveedor.add_proveedor','proveedor.change_proveedor',)
    model = Proveedor
    fields = ['email','telefono','calle','numero','localidad','cod_postal']
    template_name = 'proveedores/crear_proveedor.html'
    success_url = reverse_lazy('proveedores:listar_proveedores')
    success_message = 'Se editó el proveedor correctamente.'
    
                              
    
class RegistrarCuentaCorrienteProveedor(ValidarLoginYPermisosRequeridos,SuccessMessageMixin,CreateView):
    
    permission_required = ('proveedor.view_cuentacorrienteproveedor','proveedor.add_cuentacorrienteproveedor',)
    model = CuentaCorrienteProveedor
    form_class = CuentaCorrienteProveedorForm
    success_message = 'Se registró la cuenta corriente.'
    template_name = 'proveedores/crear_cuenta_corriente.html'
    success_url = reverse_lazy('proveedores:listar_proveedores')
    
class EliminarCuentaCorrienteProveedor(ValidarLoginYPermisosRequeridos,SuccessMessageMixin,DeleteView):
    
    permission_required = ('proveedor.view_cuentacorrienteproveedor','proveedor.add_cuentacorrienteproveedor','proveedor.change_cuentacorrienteproveedor','proveedor.delete_cuentacorrienteproveedor',)
    model = CuentaCorrienteProveedor
    template_name = 'proveedores/eliminar_cuenta_corriente.html'
    success_url = reverse_lazy('proveedores:listar_cuenta_corriente')
    success_message = 'Se eliminó la cuenta corriente correctamente.'
                                    
    def delete(self, request, *args, **kwargs):
        
        self.object = self.get_object()
        success_url = self.get_success_url()

        pedidos_asociados = Pedidos.objects.filter(cuenta_corriente = self.object.id)
    
        if len(pedidos_asociados) > 0:
            messages.add_message(request, messages.ERROR, 'No es posible eliminar una cuenta corriente con registros')
            return redirect('clientes:listar_cuenta_corriente')
        else:
            try:
                self.object.delete()
            except ProtectedError:
                messages.add_message(request, messages.ERROR, 'No se puede eliminar: Esta cuenta corriente esta relacionada.')
                return redirect('clientes:listar_cuenta_corriente')
            
        return HttpResponseRedirect(success_url) 
    
class CambiarEstadoProveedor(ValidarLoginYPermisosRequeridos, SuccessMessageMixin, UpdateView):
    
    permission_required = ('proveedor.view_proveedor','proveedor.add_proveedor',)
    model = Proveedor
    fields = ['estado']
    template_name = 'proveedores/cambiar_estado.html'
    success_url = reverse_lazy('proveedores:listar_proveedores')
    success_message = 'Se cambió el estado del proveedor correctamente.'
    
    

def verRegistro(request, cuentacorriente):
    
    queryset = Pedidos.objects.filter(cuenta_corriente = cuentacorriente)
    lista = []
    
    for registro in queryset:
        
        
        lista.append(registro)
        
    return render(request, 'proveedores/ver_registro.html', locals())
        
        
class CambiarEstadoCuentaCorriente(ValidarLoginYPermisosRequeridos,SuccessMessageMixin,UpdateView):
    
    permission_required = ('proveedor.view_cuentacorrienteproveedor','proveedor.add_cuentacorrienteproveedor','proveedor.change_cuentacorrienteproveedor',)
    model = CuentaCorrienteProveedor
    fields = ['estado']
    template_name = 'proveedores/cambiar_estado_cuenta.html'
    success_url = reverse_lazy('proveedores:listar_cuenta_corriente')
    success_message = 'Se editó el estado de la cuenta correctamente.'
    
    
    