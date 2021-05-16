from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import Categoria, SubCategoria, UnidadDeMedida, Estado, Item, Pedidos
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, ListView, FormView
from usuario.mixins import ValidarLoginYPermisosRequeridos
from .forms import ItemForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import F,ProtectedError
from django.http import HttpResponse
from ProyectoPRISMA.tasks import Pedido



class ListadoItem(ValidarLoginYPermisosRequeridos, ListView):
    permission_required = ('item.view_item',)
    model = Item
    template_name = 'items/listar_item.html'


class RegistrarItem(ValidarLoginYPermisosRequeridos, CreateView):
    permission_required = ('item.view_item', 'item.add_item',)
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


class EditarItem(ValidarLoginYPermisosRequeridos, UpdateView):

    permission_required = (
        'item.view_item', 'item.add_item', 'item.change_item',)
    model = Item
    fields = ['descripcion', 'estado']
    template_name = 'items/editar_item.html'
    success_url = reverse_lazy('items:listar_items')


class ConfigurarReposicionItem(ValidarLoginYPermisosRequeridos, UpdateView):

    permission_required = (
        'item.view_item', 'item.add_item', 'item.change_item',)
    model = Item
    fields = ['stockMinimo', 'stockSeguridad', 'repo_por_lote']
    template_name = 'items/editar_item.html'
    success_url = reverse_lazy('items:listar_items')


class EliminarItem(ValidarLoginYPermisosRequeridos, DeleteView):

    permission_required = ('item.view_item', 'item.add_item',
                           'item.change_item', 'item.delete_item',)
    model = Item
    template_name = 'items/eliminar_item.html'
    success_url = reverse_lazy('items:listar_items')

    def delete(self, request, *args, **kwargs):
        
        self.object = self.get_object()
        success_url = self.get_success_url()

        try:
            self.object.delete()
        except ProtectedError:
            messages.add_message(request, messages.ERROR, 'No se puede eliminar: Este item esta relacionado.')
            return redirect('items:listar_items')

        return HttpResponseRedirect(success_url)

class ListarCategorias(ValidarLoginYPermisosRequeridos, ListView):

    permission_required = ('item.view_item',)
    model = Item
    template_name = 'items/elegir_proveedor.html'


class ListarPedidos(ValidarLoginYPermisosRequeridos, ListView):


    model = Pedidos
    template_name = 'items/visualizar_pedidos.html'

""" def VerPedido(request, id):

    queryset = Pedidos.objects.filter(id = id)

    return render(request, 'items/pedido_proveedor.html', {'queryset': queryset}) """


def VerPedido(request, sucursal, proveedor):

    pedido_filtrado = Pedido.objects.filter( sucursal = sucursal).filter(proveedor= proveedor)
    
    lista = []
    for item in pedido_filtrado:
        
        lista.append(item) 
   
    
    return render(request, 'items/pedido_proveedor.html',locals())

#class FormularioProveedor(v)



def CompletarPedido(request, id):
    
    item = Item.objects.get(id = id)
    item.solicitud = False 
    item.save()
    
    return redirect('items:visualizar_pedidos')


def prueba(request):

    
    return HttpResponse('<h1>CORREO ENVIADO CORRECTAMENTE</h1>')


def Pedido(request):

    queryset = Item.objects.filter(cantidad=F('stockMinimo'))

    for item in queryset:
        if item.solicitud == False:
            pedidos = Pedidos()
            pedidos.item = item
            pedidos.sucursal = item.sucursal
            pedidos.proveedor = item.categoria.prov_preferido

            pedidos.save()
           
        item.solicitud = True
        item.save()

    pedidosByProveedores = {};

    resultado = Pedidos.objects.raw("""
        SELECT id, item_id, proveedor_id, sucursal_id 
        FROM item_pedidos
        """)

    for pedido in resultado:
        pedidosByProveedores.setdefault(pedido.proveedor_id, []).append(pedido)

    alreadyListened = []
    for pedido in resultado:
        pedidosToSend = []
        for elPedido in pedidosByProveedores.get(pedido.proveedor_id):
            if(pedido.sucursal_id == elPedido.sucursal_id and elPedido not in alreadyListened):
                pedidosToSend.append(elPedido)
                alreadyListened.append(elPedido)
        print(pedidosToSend) # envio al proveedor
    
    return pedidosToSend