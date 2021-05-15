from django.shortcuts import render, redirect
from .models import  MedioDePago
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, ListView
from usuario.mixins import ValidarLoginYPermisosRequeridos
from .forms import MedioDePagoForm
from django.urls import reverse_lazy






    
class ListadoMDP(ValidarLoginYPermisosRequeridos,ListView):
     permission_required = ('item.view_item',)
     model = MedioDePago
     template_name = 'mdps/listar_mdp.html'
     
     
    
class RegistrarMDP(ValidarLoginYPermisosRequeridos,CreateView):
    permission_required = ('item.view_item','item.add_item',)
    model = MedioDePago
    form_class = MedioDePagoForm
    template_name = 'mdps/crear_mdp.html'
    success_url = reverse_lazy('mdps:listar_mdps')
    

    


class EditarMDP(ValidarLoginYPermisosRequeridos,UpdateView):
    
    permission_required = ('item.view_item','item.add_item','item.change_item',)
    model = MedioDePago
    fields = ['tipo_de_pago']
    template_name = 'mdps/crear_mdp.html'
    success_url = reverse_lazy('mdps:listar_mdps')
    
    
            
    
class EliminarMDP(ValidarLoginYPermisosRequeridos,DeleteView):
    
    permission_required = ('item.view_item','item.add_item','item.change_item','item.delete_item',)
    model = MedioDePago
    template_name = 'mdps/eliminar_mdp.html'
    success_url = reverse_lazy('mdps:listar_mdps')
