from django.shortcuts import render, HttpResponseRedirect, redirect
from .forms import PresupuestoForm
from .models import Presupuesto
from django.views.generic import  CreateView, UpdateView, DeleteView, ListView
from usuario.mixins import ValidarLoginYPermisosRequeridos
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import ProtectedError



class ListadoPresupuesto(ValidarLoginYPermisosRequeridos,ListView):
    
    model = Presupuesto
    template_name = 'presupuestos/listar_presupuesto.html'



class RegistrarPresupuesto(ValidarLoginYPermisosRequeridos,CreateView):
    
    model = Presupuesto
    form_class = PresupuestoForm
    template_name = 'presupuestos/crear_presupuesto.html'
    success_url = reverse_lazy('presupuestos:listar_presupuestos')
    
    
class EliminarPresupuesto(ValidarLoginYPermisosRequeridos,DeleteView):
    
    model = Presupuesto
    template_name = 'presupuestos/eliminar_presupuesto.html'
    success_url = reverse_lazy('presupuestos:listar_presupuestos')
                                    
    def delete(self, request, *args, **kwargs):
        
        self.object = self.get_object()
        success_url = self.get_success_url()

        try:
            self.object.delete()
        except ProtectedError:
            messages.add_message(request, messages.ERROR, 'No se puede eliminar: Este presupuesto esta relacionado.')
            return redirect('presupuestos:listar_presupuestos')

        return HttpResponseRedirect(success_url)                                