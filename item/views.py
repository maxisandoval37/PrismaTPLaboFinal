from proveedor.models import Proveedor
from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import Categoria, SubCategoria,  Item, Pedidos
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, ListView
from usuario.mixins import ValidarLoginYPermisosRequeridos
from .forms import ItemForm
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.db.models import  ProtectedError
from django.http import HttpResponse
from venta.models import Venta, ItemVenta
from django.core.exceptions import ValidationError
from django.contrib.messages.views import SuccessMessageMixin
from sucursal.models import Caja, Operacion



class ListadoItem(ValidarLoginYPermisosRequeridos, ListView):
    
    permission_required = ('item.view_item',)
    model = Item
    template_name = 'items/listar_item.html'


class RegistrarItem(ValidarLoginYPermisosRequeridos, SuccessMessageMixin,CreateView):
    permission_required = ('item.view_item', 'item.add_item',)
    model = Item
    context_object_name = 'obj'
    form_class = ItemForm
    success_message = 'Item registrado correctamente.'
    template_name = 'items/crear_item.html'

    success_url = reverse_lazy('items:listar_items')

    def get_context_data(self, **kwargs):
        context = super(RegistrarItem, self).get_context_data(**kwargs)
        context["categoria"] = Categoria.objects.all()
        context["subcategoria"] = SubCategoria.objects.all()
        return context


class EditarItem(ValidarLoginYPermisosRequeridos, SuccessMessageMixin,UpdateView):

    permission_required = ('item.view_item','item.change_item')
    model = Item
    fields = ['descripcion', 'estado']
    template_name = 'items/editar_item.html'
    success_message = 'Se editó el item correctamente.'
    success_url = reverse_lazy('items:listar_items')


class ConfigurarReposicionItem(ValidarLoginYPermisosRequeridos, SuccessMessageMixin,UpdateView):

    permission_required = ('item.view_item','item.add_item','item.change_item','item.delete_item',)
    model = Item
    fields = ['stockminimo', 'stockseguridad', 'repo_por_lote']
    template_name = 'items/editar_item.html'
    success_message = 'Se configuró la reposición correctamente.'
    success_url = reverse_lazy('items:listar_items')

    def clean(self):
        if self.stockMinimo < 0:
            raise ValidationError('EL STOCK MINIMO NO PUEDE SER NEGATIVO!')
        if self.stockSeguridad < 0:
            raise ValidationError(
                'EL STOCK DE SEGURIDAD NO PUEDE SER NEGATIVO!')


class EliminarItem(ValidarLoginYPermisosRequeridos, SuccessMessageMixin,DeleteView):
    
    permission_required = ('item.view_item','item.delete_item',)
    model = Item
    template_name = 'items/eliminar_item.html'
    success_url = reverse_lazy('items:listar_items')
    success_message = 'Se eliminó el item.'

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
    
class ModificarCampos(ValidarLoginYPermisosRequeridos, ListView):
    
    permission_required = ('item.view_item','item.add_item','item.change_item','item.delete_item',)
    model = Categoria
    template_name = 'items/ver_categorias.html'


class ListarPedidos(ValidarLoginYPermisosRequeridos, ListView):

    permission_required = ('item.view_pedidos',)
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
        total = 0
        reintentos = True

        itemFromQuery = Item.objects.filter(
            nombre=itemReq, sucursal=id_sucursal)
        
        queryset = Proveedor.objects.filter(id = id_proveedor)
        razon_social = ""
        for ven in queryset:
            razon_social = ven.razon_social
        
        cajas = Caja.objects.filter(sucursal_id = id_sucursal)
        
      
        caja_mayor = None
        saldo_maximo = 0
        
        for caja in cajas:
            if caja.saldo_disponible > saldo_maximo:
                saldo_maximo = caja.saldo_disponible
                caja_mayor = caja
            else:
                caja_mayor = caja                

        print(caja_mayor)
        print(caja_mayor.egresos)
        
        for item in itemFromQuery:
            

            total = item.precio * int(cantidadReq)
            print(itemReq)
            print(cantidadReq)
            print(item.precio)
            print(total)
            
            while reintentos:
            
                if caja_mayor.saldo_disponible >= total:
                    print(caja_mayor)
                    print(caja_mayor.saldo_disponible)
                    print(total)
                    caja_mayor.saldo_disponible -= total
                    print(caja_mayor.egresos)
                    caja_mayor.egresos += total
                    print(caja_mayor.egresos)
                    print(caja_mayor.saldo_disponible)
                    caja_mayor.save()
                    item.cantidad += int(cantidadReq)
                    item.solicitud = False
                    item.save()
                    Pedidos.objects.filter(item_id=item.id).delete()
                    movimiento = Operacion()
                    movimiento.monto = "-" + str(total) 
                    movimiento.tipo= "Pedido"
                    movimiento.identificador = "Proveedor: " + razon_social
                    movimiento.save()
                    reintentos = False
            
                else:
                    if int(cantidadReq) >= 0:
                        if int(cantidadReq) == 0:
                            cantidadReq = 0
                            total = 0
                        print(cantidadReq)
                        print(total)
                        cantidadReq = int(cantidadReq) - 1
                        
                        total = item.precio * int(cantidadReq)
                        
                        print(cantidadReq)
                        print(total)
                     
    return HttpResponse("")


def CambioMasivo(request):
    
    if request.is_ajax():
        
        categoria = request.POST.get('categoria', None)
        precio = request.POST.get('precio', None)
        stock = request.POST.get('stock', None)
    
    
        items = Item.objects.filter(categoria = int(categoria))
        
        for item in items:
            
            item.precio += int(precio)
            item.stockseguridad = int(stock) 
            item.save()
            
    messages.success(request, 'Modificación masiva realizada con éxito.')
    return HttpResponse("Cambio efectuado.")
            