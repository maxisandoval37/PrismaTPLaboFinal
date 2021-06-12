import decimal

from django.http.response import HttpResponseBadRequest
from proveedor.models import Proveedor
from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import Categoria,  PinturaNueva, PinturaUsada, ReportePrecios, SubCategoria,  Item, Pedidos, Pintura, Mezcla, MezclaUsada, ReportePrecios, ReportePreciosItems
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, ListView
from usuario.mixins import ValidarLoginYPermisosRequeridos
from .forms import ItemForm, PinturaForm, MezclaForm, MezclaUsadaForm
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.db.models import ProtectedError
from django.http import HttpResponse
from venta.models import Venta, ItemVenta
from django.core.exceptions import ValidationError
from django.contrib.messages.views import SuccessMessageMixin
from sucursal.models import Caja, Operacion
from decimal import Decimal
import random
from usuario.models import Supervisor


class ListadoItem(ValidarLoginYPermisosRequeridos, ListView):

    permission_required = ('item.view_item',)
    model = Item
    template_name = 'items/listar_item.html'
    queryset = Item.objects.all().order_by('id')


class RegistrarItem(ValidarLoginYPermisosRequeridos, SuccessMessageMixin, CreateView):
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
    


class EditarItem(ValidarLoginYPermisosRequeridos, SuccessMessageMixin, UpdateView):

    permission_required = ('item.view_item', 'item.change_item')
    model = Item
    fields = ['descripcion', 'estado']
    template_name = 'items/editar_item.html'
    success_message = 'Se editó el item correctamente.'
    success_url = reverse_lazy('items:listar_items')


class ConfigurarReposicionItem(ValidarLoginYPermisosRequeridos, SuccessMessageMixin, UpdateView):

    permission_required = ('item.view_item', 'item.add_item',
                           'item.change_item', 'item.delete_item',)
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


class EliminarItem(ValidarLoginYPermisosRequeridos, SuccessMessageMixin, DeleteView):

    permission_required = ('item.view_item', 'item.delete_item',)
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


class EliminarMezcla(ValidarLoginYPermisosRequeridos, SuccessMessageMixin, DeleteView):

    permission_required = ('item.view_item', 'item.delete_item',)
    model = Mezcla
    template_name = 'items/eliminar_mezcla.html'
    success_url = reverse_lazy('items:listar_mezclas')
    success_message = 'Se eliminó la mezcla.'

    def delete(self, request, *args, **kwargs):

        self.object = self.get_object()
        success_url = self.get_success_url()

        try:
            self.object.delete()
        except ProtectedError:
            messages.add_message(
                request, messages.ERROR, 'No se puede eliminar: Esta mezcla esta relacionada.')
            return redirect('items:listar_mezclas')

        return HttpResponseRedirect(success_url)


class EliminarMezclaUsada(ValidarLoginYPermisosRequeridos, SuccessMessageMixin, DeleteView):

    permission_required = ('item.view_item', 'item.delete_item',)
    model = MezclaUsada
    template_name = 'items/eliminar_mezcla_usada.html'
    success_url = reverse_lazy('items:listar_mezclas_usadas')
    success_message = 'Se eliminó la mezcla.'

    def delete(self, request, *args, **kwargs):

        self.object = self.get_object()
        success_url = self.get_success_url()

        try:
            self.object.delete()
        except ProtectedError:
            messages.add_message(
                request, messages.ERROR, 'No se puede eliminar: Esta mezcla esta relacionada.')
            return redirect('items:listar_mezclas_usadas')

        return HttpResponseRedirect(success_url)


class ListarCategorias(ValidarLoginYPermisosRequeridos, ListView):

    permission_required = ('item.view_item', 'item.add_item',
                           'item.change_item', 'item.delete_item',)
    model = Item
    template_name = 'items/elegir_proveedor.html'
    queryset = Item.objects.all().order_by('id')


class ModificarCampos(ValidarLoginYPermisosRequeridos, ListView):

    permission_required = ('item.view_item', 'item.add_item',
                           'item.change_item', 'item.delete_item',)
    model = Categoria
    template_name = 'items/ver_categorias.html'
    queryset = Categoria.objects.all().order_by('id')
    
class ModificarCamposItems(ValidarLoginYPermisosRequeridos, ListView):

    permission_required = ('item.view_item', 'item.add_item',
                            'item.change_item', 'item.delete_item',)
    model = Item
    template_name = 'items/ver_items.html'
    queryset = Item.objects.all().order_by('id')


class ListarPedidos(ValidarLoginYPermisosRequeridos, ListView):

    permission_required = ('item.view_pedidos',)
    model = Pedidos
    template_name = 'items/visualizar_pedidos.html'
    queryset = Pedidos.objects.all().order_by('id')


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

        queryset = Proveedor.objects.filter(id=id_proveedor)
        razon_social = ""
        for ven in queryset:
            razon_social = ven.razon_social

        cajas = Caja.objects.filter(sucursal_id=id_sucursal)
        supervisorlista = Supervisor.objects.filter(sucursal_id = id_sucursal)
        supervisor = ""
        for supervisor in supervisorlista:
            supervisor = supervisor.id

        caja_mayor = None
        saldo_maximo = 0

        for caja in cajas:
            if caja.saldo_disponible > saldo_maximo:
                saldo_maximo = caja.saldo_disponible
                caja_mayor = caja
            else:
                caja_mayor = caja

        for item in itemFromQuery:

            total = item.precio * int(cantidadReq)

            while reintentos:

                if caja_mayor.saldo_disponible >= total:

                    Pedidos.objects.filter(item=item.id).update(total=total)
                    caja_mayor.saldo_disponible -= total
                    caja_mayor.egresos += total
                    caja_mayor.save()
                    item.cantidad += int(cantidadReq)
                    item.solicitud = False
                    item.save()
                    movimiento = Operacion()
                    movimiento.monto = "-" + str(total)
                    movimiento.tipo = "Pedido"
                    movimiento.caja_asociada = caja_mayor
                    movimiento.identificador = "Proveedor: " + razon_social
                    movimiento.responsable = supervisor
                    movimiento.save()
                    reintentos = False

                else:
                    if int(cantidadReq) >= 0:
                        if int(cantidadReq) == 0:
                            cantidadReq = 0
                            total = 0
                        cantidadReq = int(cantidadReq) - 1

                        total = item.precio * int(cantidadReq)

    return HttpResponse("")


def CambioMasivo(request):

    if request.is_ajax():

        categoria = request.POST.get('categoria', None)
        precio = request.POST.get('precio', None)
        stock = request.POST.get('stock', None)
        items = Item.objects.filter(categoria=int(categoria))
        
        if precio == '':
            precio = "vacio"
        else:
            if not precio.isdigit():
                return HttpResponseBadRequest()
        if stock == '':
            stock = "vacio"
        else:
            if not stock.isdigit():
                return HttpResponseBadRequest()
        
        if precio != "vacio":
            if int(precio) < 0:
                return HttpResponseBadRequest()
            if int(precio) > 99999:
                return HttpResponseBadRequest()
        if stock != "vacio":
            if int(stock) < 0:
                return HttpResponseBadRequest()
            if int(stock) > 99999:
                return HttpResponseBadRequest()
            
        reporte_precios = ReportePrecios()
        reporte_precios.categoria_asociada_id = int(categoria)
        if precio == "vacio":
            reporte_precios.aumento = 0
        else:
            reporte_precios.aumento = int(precio)
        reporte_precios.responsable_id = request.user.id
        reporte_precios.save()

        for item in items:
            if precio != "vacio":
                item.precio += int(precio)
            if stock != "vacio":
                item.stockseguridad = int(stock)
            item.save()

    messages.success(request, 'Modificación masiva realizada con éxito.')
    return HttpResponse("Cambio efectuado.")

def CambioMasivoItems(request):

    if request.is_ajax():

        precio = request.POST.get('precio', None)
        items = Item.objects.all()
        
        if precio == '':
            precio = "vacio"
        else:
            if not precio.isdigit():
                return HttpResponseBadRequest()
       
        
        if precio != "vacio":
            if int(precio) < 0:
                return HttpResponseBadRequest()
            if int(precio) > 99999:
                return HttpResponseBadRequest()
       
            
        reporte_precios = ReportePreciosItems()
        
        if precio == "vacio":
            reporte_precios.aumento = 0
        else:
            reporte_precios.aumento = int(precio)
        reporte_precios.responsable_id = request.user.id
        reporte_precios.save()

        for item in items:
            if precio != "vacio":
                item.precio += int(precio)
            else:
                messages.error(request, 'Debes ingresar un monto para realizar la modificación masiva.')
                
            item.save()

    messages.success(request, 'Modificación masiva realizada con éxito.')
    return HttpResponse("Cambio efectuado.")


class ListadoPintura(ValidarLoginYPermisosRequeridos, ListView):

    model = Pintura
    template_name = 'items/listar_pintura.html'
    queryset = Pintura.objects.all().order_by('id')


class ListadoPinturaNueva(ValidarLoginYPermisosRequeridos, ListView):

    model = PinturaNueva
    template_name = 'items/listar_pintura_nueva.html'
    queryset = PinturaNueva.objects.all().order_by('id')


class ListadoPinturaUsada(ValidarLoginYPermisosRequeridos, ListView):

    model = PinturaUsada
    template_name = 'items/listar_pintura_usada.html'
    queryset = PinturaUsada.objects.all().order_by('id')


class AgregarPintura(ValidarLoginYPermisosRequeridos, SuccessMessageMixin, CreateView):

    model = Pintura
    form_class = PinturaForm
    template_name = 'items/crear_pintura.html'
    success_message = 'Pintura registrada con éxito.'
    success_url = reverse_lazy('items:listar_pinturas')


class ListadoMezclas(ValidarLoginYPermisosRequeridos, ListView):

    model = Mezcla
    template_name = 'items/listar_mezcla.html'
    queryset = Mezcla.objects.all().order_by('id')


class IniciarMezcla(ValidarLoginYPermisosRequeridos, SuccessMessageMixin, CreateView):

    model = Mezcla
    form_class = MezclaForm
    template_name = 'items/iniciar_mezcla.html'
    success_message = 'Mezcla realizada correctamente.'
    success_url = reverse_lazy('items:listar_mezclas')


class ListadoMezclaUsada(ValidarLoginYPermisosRequeridos, ListView):

    model = MezclaUsada
    template_name = 'items/listar_mezcla_usada.html'
    queryset = MezclaUsada.objects.all().order_by('id')


class IniciarMezclaUsada(ValidarLoginYPermisosRequeridos, SuccessMessageMixin, CreateView):

    model = MezclaUsada
    form_class = MezclaUsadaForm
    template_name = 'items/iniciar_mezcla_usada.html'
    success_message = 'Mezcla realizada correctamente.'
    success_url = reverse_lazy('items:listar_mezclas_usadas')


def mezclarPinturas(request, mezcla, primerapintura, segundapintura, cantidad_primera, cantidad_segunda):

    queryset1 = Pintura.objects.filter(id=primerapintura)
    queryset2 = Pintura.objects.filter(id=segundapintura)
    primera_pintura = None
    segunda_pintura = None

    for pintura in queryset1:
        primera_pintura = pintura
    for pintura in queryset2:
        segunda_pintura = pintura

    if primera_pintura.cantidad - 1 < 0 or segunda_pintura.cantidad - 1 < 0:
        messages.error(
            request, 'No hay stock disponible para realizar la mezcla.')
        return redirect('items:listar_mezclas')

    pintura = PinturaNueva.objects.filter(color=primera_pintura.color + " y " + segunda_pintura.color +
                                          " | Cantidad: " + str(cantidad_primera) + " | " + str(cantidad_segunda))

    if len(pintura) > 0:

        for p in pintura:

            p.stock += 1
            p.save()
    else:

        nueva_pintura = PinturaNueva()
        nueva_pintura.codigo_de_barras = random.randint(
            999999999999, 10000000000000)
        nueva_pintura.pcant = cantidad_primera
        nueva_pintura.scant = cantidad_segunda
        nueva_pintura.nombre = "Pintura " + \
            primera_pintura.color + " y " + segunda_pintura.color
        nueva_pintura.color = primera_pintura.color + " y " + segunda_pintura.color + \
            " | Cantidad: " + str(nueva_pintura.pcant) + \
            " | " + str(nueva_pintura.scant)
        nueva_pintura.precio = primera_pintura.precio + segunda_pintura.precio + \
            ((primera_pintura.precio + segunda_pintura.precio)
             * Decimal("0.10".replace(',', '.')))
        nueva_pintura.cantidad = cantidad_primera + cantidad_segunda
        nueva_pintura.sucursal = primera_pintura.sucursal
        nueva_pintura.stock = 1
        nueva_pintura.save()

    usada_uno = PinturaUsada.objects.filter(
        nombre=primera_pintura.nombre, color=primera_pintura.color)
    usada_dos = PinturaUsada.objects.filter(
        nombre=segunda_pintura.nombre, color=segunda_pintura.color)

    if len(usada_uno) > 0:
        for usada in usada_uno:
            usada.cantidad_restante += (
                primera_pintura.cantidad_pintura - cantidad_primera)
            usada.save()
    else:
        pintura_usada = PinturaUsada()
        pintura_usada.codigo_de_barras = random.randint(
            999999999999, 10000000000000)
        pintura_usada.nombre = primera_pintura.nombre
        pintura_usada.color = primera_pintura.color
        pintura_usada.cantidad_restante = primera_pintura.cantidad_pintura - cantidad_primera
        pintura_usada.precio = primera_pintura.precio
        pintura_usada.sucursal = primera_pintura.sucursal
        pintura_usada.save()

    if len(usada_dos) > 0:
        for usada in usada_dos:
            usada.cantidad_restante += (
                segunda_pintura.cantidad_pintura - cantidad_segunda)
            usada.save()
    else:
        segunda_usada = PinturaUsada()
        segunda_usada.codigo_de_barras = random.randint(
            999999999999, 10000000000000)
        segunda_usada.nombre = segunda_pintura.nombre
        segunda_usada.color = segunda_pintura.color
        segunda_usada.cantidad_restante = segunda_pintura.cantidad_pintura - cantidad_segunda
        segunda_usada.precio = segunda_pintura.precio
        segunda_usada.sucursal = segunda_pintura.sucursal
        segunda_usada.save()

    primera_pintura.cantidad -= 1
    primera_pintura.save()
    segunda_pintura.cantidad -= 1
    segunda_pintura.save()

    Mezcla.objects.filter(id=mezcla).delete()

    messages.success(request, 'Mezcla finalizada con éxito.')
    return redirect('items:listar_pinturas')


def mezclarPinturasUsadas(request, mezcla, primerapintura, segundapintura, cantidad_primera, cantidad_segunda):

    queryset1 = PinturaUsada.objects.filter(id=primerapintura)
    queryset2 = PinturaUsada.objects.filter(id=segundapintura)
    primera_pintura = None
    segunda_pintura = None

    for pintura in queryset1:
        primera_pintura = pintura
    for pintura in queryset2:
        segunda_pintura = pintura

    pintura = PinturaNueva.objects.filter(color=primera_pintura.color + " y " + segunda_pintura.color +
                                          " | Cantidad: " + str(cantidad_primera) + " | " + str(cantidad_segunda))

    if len(pintura) > 0:

        for p in pintura:

            p.stock += 1
            p.save()
    else:

        nueva_pintura = PinturaNueva()
        nueva_pintura.codigo_de_barras = random.randint(
            999999999999, 10000000000000)
        nueva_pintura.pcant = cantidad_primera
        nueva_pintura.scant = cantidad_segunda
        nueva_pintura.nombre = "Pintura " + \
            primera_pintura.color + " y " + segunda_pintura.color
        nueva_pintura.color = primera_pintura.color + " y " + segunda_pintura.color + \
            " | Cantidad: " + str(nueva_pintura.pcant) + \
            " | " + str(nueva_pintura.scant)
        nueva_pintura.precio = primera_pintura.precio + segunda_pintura.precio + \
            ((primera_pintura.precio + segunda_pintura.precio)
             * Decimal("0.10".replace(',', '.')))
        nueva_pintura.cantidad = cantidad_primera + cantidad_segunda
        nueva_pintura.sucursal = primera_pintura.sucursal
        nueva_pintura.stock = 1
        nueva_pintura.save()

    primera_pintura.cantidad_restante -= cantidad_primera
    segunda_pintura.cantidad_restante -= cantidad_segunda
    primera_pintura.save()
    segunda_pintura.save()

    MezclaUsada.objects.filter(id=mezcla).delete()

    if primera_pintura.cantidad_restante == 0:
        primera_pintura.delete()
    if segunda_pintura.cantidad_restante == 0:
        segunda_pintura.delete()

    messages.success(request, 'Mezcla realizada con éxito.')
    return redirect('items:listar_mezclas_usadas')


def ReporteItemRiesgoStock(request):
    queryset = Item.objects.all()
    items = []

    for item in queryset:
        items.append(item)

    return render(request, 'items/reporte_riesgo_stock.html', locals())


def ReporteCambiosPrecios(request):
    queryset = ReportePrecios.objects.all()
    filas = []

    for fila in queryset:
        print("fila.aumento")
        print(fila.aumento)
        dic = {
            "id": fila.id,
            "fecha": fila.fecha,
            "categoria": fila.categoria_asociada.opciones,
            "aumento": fila.aumento,
            "responsable": fila.responsable.nombre,
            "fecha_a_comparar": str(fila.fecha.date())
        }
        filas.append(dic)

    return render(request, 'items/reporte_cambios_masivos.html', locals())

def ReporteCuentaCorrienteProveedores(request):
    queryset = Pedidos.objects.all()
    listaPedidos = []

    for pedido in queryset:
        listaPedidos.append(pedido)

    return render(request,'items/reporte_cuenta_corriente_proveedores.html',locals())