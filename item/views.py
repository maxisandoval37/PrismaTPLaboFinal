from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import Categoria, SubCategoria,  Item, Pedidos
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, ListView
from usuario.mixins import ValidarLoginYPermisosRequeridos
from .forms import ItemForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import  ProtectedError
from django.http import HttpResponse
from venta.models import Venta
from django.core.exceptions import ValidationError




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

    permission_required = ('item.view_item','item.change_item')
    model = Item
    fields = ['descripcion', 'estado']
    template_name = 'items/editar_item.html'
    success_url = reverse_lazy('items:listar_items')


class ConfigurarReposicionItem(ValidarLoginYPermisosRequeridos, UpdateView):

    permission_required = ('item.view_item','item.add_item','item.change_item','item.delete_item',)
    model = Item
    fields = ['stockminimo', 'stockseguridad', 'repo_por_lote']
    template_name = 'items/editar_item.html'
    success_url = reverse_lazy('items:listar_items')

    def clean(self):
        if self.stockMinimo < 0:
            raise ValidationError('EL STOCK MINIMO NO PUEDE SER NEGATIVO!')
        if self.stockSeguridad < 0:
            raise ValidationError(
                'EL STOCK DE SEGURIDAD NO PUEDE SER NEGATIVO!')


class EliminarItem(ValidarLoginYPermisosRequeridos, DeleteView):
    
    permission_required = ('item.view_item','item.delete_item',)
    model = Item
    template_name = 'items/eliminar_item.html'
    success_url = reverse_lazy('items:listar_items')

    def delete(self, request, *args, **kwargs):

        self.object = self.get_object()
        success_url = self.get_success_url()

        try:
            self.object.delete()
        except ProtectedError:
            messages.add_message(
                request, messages.ERROR, 'No se puede eliminar: Este item esta relacionado.')
            return redirect('items:listar_items')

        return HttpResponseRedirect(success_url)


class ListarCategorias(ValidarLoginYPermisosRequeridos, ListView):
    

    permission_required = ('item.view_item','item.add_item','item.change_item','item.delete_item',)
    model = Item
    template_name = 'items/elegir_proveedor.html'


class ListarPedidos(ValidarLoginYPermisosRequeridos, ListView):

    permission_required = ('item.view_item','item.add_item','item.change_item','item.delete_item',)
    model = Pedidos
    template_name = 'items/visualizar_pedidos.html'


class MensajeExitoso(TemplateView):
    
    template_name = 'items/stock_recibido.html'
    

def VerPedido(request, id_proveedor, id_sucursal):
    queryset = Pedidos.objects.filter(
        proveedor_id=id_proveedor).filter(sucursal_id=id_sucursal)
    return render(request, 'items/pedido_proveedor.html', {'queryset': queryset})


def RecibirStock(request, id_proveedor, id_sucursal):
    if request.is_ajax():
        itemReq = request.POST.get('item', None)
        cantidadReq = request.POST.get('cantidad', None)
        print(itemReq)
        print(cantidadReq)

        itemFromQuery = Item.objects.filter(
            nombre=itemReq, sucursal=id_sucursal)
        print(itemFromQuery)

        for item in itemFromQuery:
            item.cantidad += int(cantidadReq)
            item.solicitud = False
            item.save()
            Pedidos.objects.filter(item_id=item.id).delete()

    return HttpResponse("Pedido recibido exitosamente!")