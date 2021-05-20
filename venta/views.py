from django.shortcuts import render, HttpResponseRedirect, redirect
from .forms import VentaLocalForm, VentaVirtualForm
from .models import VentaLocal, VentaVirtual, Venta
from django.views.generic import  CreateView,  DeleteView, ListView
from usuario.mixins import ValidarLoginYPermisosRequeridos
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import ProtectedError



class ListadoVenta(ValidarLoginYPermisosRequeridos,ListView):
    
    model = Venta
    template_name = 'ventas/listar_venta.html'



class RegistrarVentaLocal(ValidarLoginYPermisosRequeridos,CreateView):
    
    model = VentaLocal
    form_class = VentaLocalForm
    template_name = 'ventas/crear_venta_local.html'
    success_url = reverse_lazy('ventas:listar_venta')
    
class RegistrarVentaVirtual(ValidarLoginYPermisosRequeridos,CreateView):
    
    model = VentaVirtual
    form_class = VentaVirtualForm
    template_name = 'ventas/crear_venta_virtual.html'
    success_url = reverse_lazy('ventas:listar_venta')
    
    
    
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