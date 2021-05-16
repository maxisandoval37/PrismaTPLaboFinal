from django.shortcuts import render, redirect
from .models import Categoria, SubCategoria, UnidadDeMedida, Estado, Item, Pedidos
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, ListView, FormView
from usuario.mixins import ValidarLoginYPermisosRequeridos
from .forms import ItemForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponse
from ProyectoPRISMA.tasks import sleepy, enviar_correo, setup_periodic_tasks
from django.db.models import F, Count


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


class ListarCategorias(ValidarLoginYPermisosRequeridos, ListView):

    permission_required = ('item.view_item',)
    model = Item
    template_name = 'items/elegir_proveedor.html'


class ListarPedidos(ValidarLoginYPermisosRequeridos, ListView):


    model = Pedidos
    template_name = 'items/visualizar_pedidos.html'


def CompletarPedido(request, id):
    
    item = Item.objects.get(id = id)
    item.solicitud = False 
    item.save()
    
    return redirect('items:visualizar_pedidos')


""" def prueba(request):

    return HttpResponse('<h1>CORREO ENVIADO CORRECTAMENTE</h1>') """


def Pedido(request):

    queryset = Item.objects.filter(cantidad=F('stockMinimo'))

    lista = []
    for item in queryset:
        if item.solicitud == False:
            pedidos = Pedidos()
            pedidos.item = item
            pedidos.sucursal = item.sucursal
            pedidos.proveedor = item.categoria.prov_preferido

            pedidos.save()
            lista.append(pedidos)
        item.solicitud = True
        item.save()

    resultado = Pedidos.objects.values('sucursal', 'proveedor').order_by(
    ).annotate(Count('sucursal'), Count('proveedor'))
    print(resultado)

    return render(request, 'items/visualizar_pedidos.html', locals())
