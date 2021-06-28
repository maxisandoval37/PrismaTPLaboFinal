from django.shortcuts import render, HttpResponseRedirect, redirect
from .forms import ClienteForm, CuentaCorrienteForm, MedioDePagoForm
from .models import Cliente, CuentaCorriente, MedioDePago
from django.views.generic import  CreateView, UpdateView, DeleteView, ListView
from usuario.mixins import ValidarLoginYPermisosRequeridos
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from venta.models import Venta
from django.db.models import ProtectedError
from django.core.exceptions import ValidationError

class ListadoCliente(ValidarLoginYPermisosRequeridos,ListView):
    
    permission_required = ('cliente.view_cliente',)
    model = Cliente
    template_name = 'clientes/listar_cliente.html'
    queryset = Cliente.objects.all().order_by('id')

class ListadoCuentasCorriente(ValidarLoginYPermisosRequeridos, ListView):
    
    permission_required = ('cliente.view_cuentacorriente',)
    model = CuentaCorriente
    template_name = 'clientes/listar_cuenta_corriente.html'
    queryset = CuentaCorriente.objects.all().order_by('numero_cuenta')

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
    fields = ['email','telefono','categoria_cliente']
    success_message = 'Se editó al cliente correctamente.'
    template_name = 'clientes/crear_cliente.html'
    success_url = reverse_lazy('clientes:listar_clientes')
 
    
class DesactivarCliente(ValidarLoginYPermisosRequeridos, SuccessMessageMixin, UpdateView):
    
    permission_required = ('cliente.view_cliente','cliente.change_cliente',)
    model = Cliente
    fields = ['estado_cliente']
    success_message = 'Se cambio el estado del cliente correctamente.'
    template_name = 'clientes/editar_cliente.html'
    success_url = reverse_lazy('clientes:listar_clientes')
 
    
    

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
    
    
class EliminarCuentaCorriente(ValidarLoginYPermisosRequeridos,SuccessMessageMixin,DeleteView):
    
    permission_required = ('cliente.view_cuentacorriente','cliente.add_cuentacorriente',)
    model = CuentaCorriente
    template_name = 'clientes/eliminar_cuenta_corriente.html'
    success_url = reverse_lazy('clientes:listar_cuenta_corriente')
    success_message = 'Se eliminó la cuenta corriente correctamente.'
                                    
    def delete(self, request, *args, **kwargs):
        
        self.object = self.get_object()
        success_url = self.get_success_url()

        ventas_asociadas = Venta.objects.filter(cuenta_corriente = self.object.id)
        
        if len(ventas_asociadas) > 0:
            messages.add_message(request, messages.ERROR, 'No es posible eliminar una cuenta corriente con registros')
            return redirect('clientes:listar_cuenta_corriente')
        else:
            try:
                self.object.delete()
            except ProtectedError:
                messages.add_message(request, messages.ERROR, 'No se puede eliminar: Esta cuenta corriente esta relacionada.')
                return redirect('clientes:listar_cuenta_corriente')

        return HttpResponseRedirect(success_url) 
    

def verRegistro(request, cuentacorriente):
    
    queryset = Venta.objects.filter(cuenta_corriente = cuentacorriente).order_by('numero_comprobante')
    lista = []
    
    for registro in queryset:
        
        
        if registro.estado.opciones == 'PAGADA':
            lista.append(registro)
        
    return render(request, 'clientes/ver_registro.html', locals())

def consultaDiaria(request):
    return render(request, 'clientes/consultas_cotizaciones.html')


def consultaHistorico(request):
    return render(request, 'clientes/consultas_historico.html')


class CambiarEstadoCuentaCorriente(ValidarLoginYPermisosRequeridos,SuccessMessageMixin,UpdateView):
    
    permission_required = ('cliente.view_cuentacorriente','cliente.change_cuentacorriente',)
    model = CuentaCorriente
    fields = ['estado']
    template_name = 'clientes/cambiar_estado_cuenta.html'
    success_url = reverse_lazy('clientes:listar_cuenta_corriente')
    success_message = 'Se editó el estado de la cuenta correctamente.'
