from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import  MedioDePago
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, ListView
from usuario.mixins import ValidarLoginYPermisosRequeridos
from .forms import MedioDePagoForm
from django.urls import reverse_lazy
from django.db.models import ProtectedError
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin



    
class ListadoMDP(ValidarLoginYPermisosRequeridos,ListView):
     permission_required = ('item.view_item',)
     model = MedioDePago
     template_name = 'mdps/listar_mdp.html'
     
     
    
class RegistrarMDP(ValidarLoginYPermisosRequeridos,SuccessMessageMixin,CreateView):
    permission_required = ('item.view_item','item.add_item',)
    model = MedioDePago
    form_class = MedioDePagoForm
    template_name = 'mdps/crear_mdp.html'
    success_message = 'Medio de pago registrado con éxito.'
    success_url = reverse_lazy('mdps:listar_mdps')
    

    


class EditarMDP(ValidarLoginYPermisosRequeridos,SuccessMessageMixin,UpdateView):
    
    permission_required = ('item.view_item','item.add_item','item.change_item',)
    model = MedioDePago
    fields = ['tipo_de_pago']
    template_name = 'mdps/crear_mdp.html'
    success_message = 'Se editó el medio de pago correctamente.'
    success_url = reverse_lazy('mdps:listar_mdps')
    
    
            
    
class EliminarMDP(ValidarLoginYPermisosRequeridos,SuccessMessageMixin,DeleteView):
    
    permission_required = ('item.view_item','item.add_item','item.change_item','item.delete_item',)
    model = MedioDePago
    template_name = 'mdps/eliminar_mdp.html'
    success_message = 'Se eliminó el medio de pago.'
    success_url = reverse_lazy('mdps:listar_mdps')


    def delete(self, request, *args, **kwargs):
        
        self.object = self.get_object()
        success_url = self.get_success_url()

        try:
            self.object.delete()
        except ProtectedError:
            messages.add_message(request, messages.ERROR, 'No se puede eliminar: Este medio de pago esta relacionado.')
            return redirect('items:listar_items')

        return HttpResponseRedirect(success_url)
