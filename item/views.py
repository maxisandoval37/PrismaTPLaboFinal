from django.shortcuts import render, redirect
from .models import Categoria, SubCategoria,UnidadDeMedida, Estado, Item
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, ListView, FormView
from usuario.mixins import ValidarLoginYPermisosRequeridos
from .forms import ItemForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponse
from ProyectoPRISMA.tasks import sleepy, enviar_correo





    
class ListadoItem(ValidarLoginYPermisosRequeridos,ListView):
     permission_required = ('item.view_item',)
     model = Item
     template_name = 'items/listar_item.html'
     
     
    
class RegistrarItem(ValidarLoginYPermisosRequeridos,CreateView):
    permission_required = ('item.view_item','item.add_item',)
    model = Item
    context_object_name = 'obj'
    form_class = ItemForm
    template_name = 'items/crear_item.html'
    
    success_url = reverse_lazy('items:listar_items')
    
    
    def get_context_data(self, **kwargs):
       context = super(RegistrarItem, self).get_context_data(**kwargs)
       context["categoria"] = Categoria.objects.all()
       context["subcategoria"] = SubCategoria.objects.all()
       return context
   
    


class EditarItem(ValidarLoginYPermisosRequeridos,UpdateView):
    
    permission_required = ('item.view_item','item.add_item','item.change_item',)
    model = Item
    fields = ['descripcion','estado']
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

class ListarCategorias(ValidarLoginYPermisosRequeridos,ListView):
    
     permission_required = ('item.view_item',)
     model = Item
     template_name = 'items/elegir_proveedor.html'


def prueba(request):
    
    enviar_correo()
    return HttpResponse('<h1>CORREO ENVIADO CORRECTAMENTE</h1>')




""" 
def alertaStock(request, id):
    
    if request.method == 'POST':
        item = Item.objects.get(id = id)
        if item.alerta:
            messages.success(request, "NO HAY STOCK MINIMO ")
            return redirect(to='items:listar_items')
        
  """
    
