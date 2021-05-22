from django.shortcuts import render, HttpResponseRedirect, redirect
from .forms import VentaLocalForm, VentaVirtualForm
from .models import VentaLocal, VentaVirtual, Venta
from django.views.generic import  CreateView,  DeleteView, ListView
from usuario.mixins import ValidarLoginYPermisosRequeridos
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import ProtectedError
from cliente.models import Cliente, CuentaCorriente,MedioDePago
from sucursal.models import Sucursal
from usuario.models import Vendedor, Supervisor
from django.core.exceptions import ValidationError




class ListadoVenta(ValidarLoginYPermisosRequeridos,ListView):
    
    model = Venta
    template_name = 'ventas/listar_venta.html'



class RegistrarVentaLocal(ValidarLoginYPermisosRequeridos,CreateView):
    
    model = VentaLocal
    context_object_name = 'obj'
    form_class = VentaLocalForm
    template_name = 'ventas/crear_venta_local.html'
    success_url = reverse_lazy('ventas:listar_ventas')
      
    
    def get_context_data(self, **kwargs):
        context = super(RegistrarVentaLocal, self).get_context_data(**kwargs)
        context["cliente_asociado"] = Cliente.objects.all()
        context["mediodepago"] = MedioDePago.objects.all()
        context["cuenta_corriente"] = CuentaCorriente.objects.all()
        context["sucursal_asociada"] = Sucursal.objects.all()
        context["vendedor_asociado"] = Vendedor.objects.all()
        return context
    
    
    
    
class RegistrarVentaVirtual(ValidarLoginYPermisosRequeridos,CreateView):
    
    model = VentaVirtual
    context_object_name = 'obj'
    form_class = VentaVirtualForm
    template_name = 'ventas/crear_venta_virtual.html'
    success_url = reverse_lazy('ventas:listar_ventas')
    
    def get_context_data(self, **kwargs):
        context = super(RegistrarVentaVirtual, self).get_context_data(**kwargs)
        context["cliente_asociado"] = Cliente.objects.all()
        context["mediodepago"] = MedioDePago.objects.all()
        context["cuenta_corriente"] = CuentaCorriente.objects.all()
        context["sucursal_asociada"] = Sucursal.objects.all()
        context["vendedor_asociado"] = Vendedor.objects.all()
        return context
    
class EliminarVenta(ValidarLoginYPermisosRequeridos,DeleteView):
    
    model = Venta
    template_name = 'ventas/eliminar_venta.html'
    success_url = reverse_lazy('ventas:listar_ventas')
                                    
    def delete(self, request, *args, **kwargs):
        
        self.object = self.get_object()
        success_url = self.get_success_url()

        try:
            self.object.delete()
        except ProtectedError:
            messages.add_message(request, messages.ERROR, 'No se puede eliminar: Ésta venta está relacionada.')
            return redirect('ventas:listar_ventas')

        return HttpResponseRedirect(success_url)                                
    
    
