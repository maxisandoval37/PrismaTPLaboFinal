from django.shortcuts import render
from .models import Categoria,UnidadDeMedida, Estado, Item
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, ListView, FormView
from usuario.mixins import ValidarLoginYPermisosRequeridos
from .forms import ItemForm
from django.urls import reverse_lazy





    
class ListadoItem(ValidarLoginYPermisosRequeridos,ListView):
     permission_required = ('item.view_item',)
     model = Item
     template_name = 'items/listar_item.html'
     
     
    
class RegistrarItem(ValidarLoginYPermisosRequeridos,CreateView):
    permission_required = ('item.view_item','item.add_item',)
    model = Item
    form_class = ItemForm
    template_name = 'items/crear_item.html'
    success_url = reverse_lazy('items:listar_items')
    
   


class EditarItem(ValidarLoginYPermisosRequeridos,UpdateView):
    
    permission_required = ('item.view_item','item.add_item','item.change_item',)
    model = Item
    fields = ['precio','ubicacion','unidad_de_medida','estado']
    template_name = 'items/editar_item.html'
    success_url = reverse_lazy('items:listar_items')
    
    
class ConfigurarReposicionItem(ValidarLoginYPermisosRequeridos,UpdateView):
    
    permission_required = ('item.view_item','item.add_item','item.change_item',)
    model = Item
    fields = ['stockMinimo','stockSeguridad','repo_por_lote']
    template_name = 'items/editar_item.html'
    success_url = reverse_lazy('items:listar_items')    

class EliminarItem(ValidarLoginYPermisosRequeridos,DeleteView):
    
    permission_required = ('item.view_item','item.add_item','item.change_item','item.delete_item',)
    model = Item
    template_name = 'items/eliminar_item.html'
    success_url = reverse_lazy('items:listar_items')



""" 
def convertor(request, id):
    
    item = Item.objects.get(id = id)
    if request.method == 'GET':
        item_form = ItemForm(instance = item)
    else:
        item_form = ItemForm(request.POST, istance = item)
        if item_form.is_valid():
            if item.unidad_de_medida == 'KG':
                item.precio = item.precio  """