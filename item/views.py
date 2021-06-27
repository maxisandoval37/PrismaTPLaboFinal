from django.http.response import HttpResponseBadRequest
from proveedor.models import EstadoProveedor, Proveedor
from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import Categoria,  PinturaNueva, PinturaUsada, ReportePrecios, SubCategoria,  Item, Pedidos, Pintura, Mezcla, MezclaUsada, ReportePrecios, ReportePreciosItems, HistorialPref
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, ListView
from usuario.mixins import ValidarLoginYPermisosRequeridos
from .forms import ItemForm, PinturaForm, MezclaForm, MezclaUsadaForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import ProtectedError
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.contrib.messages.views import SuccessMessageMixin
from sucursal.models import Caja, Operacion, Sucursal
from decimal import Decimal
import random
from usuario.models import Supervisor, Rol
from django.core.mail import send_mail
from proveedor.models import CuentaCorrienteProveedor
from item.models import Estado
from usuario.models import Vendedor



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
    fields = ['descripcion']
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

    permission_required = ('item.view_item',)
    model = Categoria
    context_object_name = 'obj'
    template_name = 'items/elegir_proveedor.html'
    queryset = Categoria.objects.all().order_by('id')
    
    def get_context_data(self, **kwargs):
        context = super(ListarCategorias, self).get_context_data(**kwargs)
        
        estados = EstadoProveedor.objects.filter(opciones = 'ACTIVO')
        activo = 0
        for estado in estados:
            activo = estado.id
        
        context["proveedor"] = Proveedor.objects.filter(estado = activo)
        
        return context



class ModificarCampos(ValidarLoginYPermisosRequeridos, ListView):

    permission_required = ('item.view_item', 
                           'item.change_item', )
    model = Categoria
    template_name = 'items/ver_categorias.html'
    queryset = Categoria.objects.all().order_by('id')
    
class ModificarCamposItems(ValidarLoginYPermisosRequeridos, ListView):

    permission_required = ('item.view_item', 
                            'item.change_item',)
    model = Item
    template_name = 'items/ver_items.html'
    queryset = Item.objects.all().order_by('id')


class ListarPedidos(ValidarLoginYPermisosRequeridos, ListView):

    permission_required = ('item.view_pedidos',)
    model = Pedidos
    template_name = 'items/visualizar_pedidos.html'
    queryset = Pedidos.objects.all().order_by('id')
    
class CambiarEstadoItem(ValidarLoginYPermisosRequeridos, SuccessMessageMixin, UpdateView):
    
    permission_required = ('item.view_item', 'item.add_item',)
    model = Item
    fields = ['estado']
    success_message = 'Se cambió el estado del item correctamente.'
    template_name = 'items/cambiar_estado.html'
    success_url = reverse_lazy('items:listar_items')


class MensajeExitoso(TemplateView):

    template_name = 'items/stock_recibido.html'


def VerPedido(request, id_proveedor, id_sucursal):
    queryset = Pedidos.objects.filter(
        proveedor_id=id_proveedor).filter(sucursal_id=id_sucursal).filter(estado = True)
    return render(request, 'items/pedido_proveedor.html', {'queryset': queryset})


def RecibirStock(request, id_proveedor, id_sucursal):
    
    if request.is_ajax():
        itemReq = request.POST.get('item', None)
        cantidadReq = request.POST.get('cantidad', None)
        pedido = request.POST.get('pedido', None)
        total = 0
        reintentos = True

        pedidos = Pedidos.objects.filter(id = int(pedido))
        pedido_int = int(pedido)
        
        
        for cant in cantidadReq:
            
            if cant.isalpha():
                messages.error(request, "Sólo puedes ingresar digitos.")
                return HttpResponse()
        
        if not cantidadReq.isdigit():
            messages.error(request, "Sólo puedes ingresar digitos.")
            return HttpResponse()
        
        for pedido in pedidos:
            
            if int(cantidadReq) > pedido.solicitado:
                messages.error(request, "Lo sentimos, pero no podemos recibir más de la cantidad que solicitamos.")
                return HttpResponse()
        
        if int(cantidadReq) < 0:
            messages.error(request, "No puedes ingresar una cantidad negativa.")
            return HttpResponse()
        
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
                    
                    Pedidos.objects.filter(item=item.id).filter(id = pedido_int).update(total=total)
                    Pedidos.objects.filter(item=item.id).filter(id = pedido_int).update(cantidad = int(cantidadReq))
                    Pedidos.objects.filter(item=item.id).filter(id = pedido_int).update(estado = False) 
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
                    if supervisor == '':
                        messages.error(request, "Lo sentimos, vuelve a intentarlo más tarde.")
                        return HttpResponse()
                    else:
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
        
        for p in precio:
            
            if p.isalpha():
                return HttpResponseBadRequest()
        count = 0
        for p in precio:
            
            if p == "-":
                count += 1
            if count > 1:
                return HttpResponseBadRequest()
        
        if precio != "vacio":
            
            if int(precio) > 99999:
                return HttpResponseBadRequest()

        if len(stock) != 0 and int(stock) < 0:
            return HttpResponseBadRequest()

        reporte_precios = ReportePrecios()
        reporte_precios.categoria_asociada_id = int(categoria)
        if precio == "vacio":
            reporte_precios.aumento = 0
        else:
            reporte_precios.aumento = int(precio)
        if request.user.is_staff or request.user.rol.opciones != 'SUPERVISOR':
            messages.warning(request, "Sólo el supervisor puede realizar el cambio masivo.")
            return HttpResponse()
        else:
            reporte_precios.responsable_id = request.user.id
        reporte_precios.responsable_usuario_id = request.user.id
        reporte_precios.save()

        for item in items:
            item.precio += int(precio)
            if len(stock) != 0:
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
        
        for p in precio:
            
            if p.isalpha():
                return HttpResponseBadRequest()
        count = 0
        for p in precio:
            
            if p == "-":
                count += 1
            if count > 1:
                return HttpResponseBadRequest()
        
        if precio != "vacio":
            
            if int(precio) > 99999:
                return HttpResponseBadRequest()
       
            
        reporte_precios = ReportePreciosItems()
        
        if precio == "vacio":
            reporte_precios.aumento = 0
        else:
            reporte_precios.aumento = int(precio)
        if request.user.is_staff or request.user.rol.opciones != 'SUPERVISOR':
            messages.warning(request, "Sólo el supervisor puede realizar el cambio masivo.")
            return HttpResponse()
        else:
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


def ListarPintura(request):
    

    if request.user.is_staff or request.user.rol.opciones == 'GERENTE GENERAL':
        
        lista = []
        colores = []
        pinturas = Pintura.objects.all()
        
        for pintura in pinturas:
            
            if pintura.color not in colores:
                
                colores.append(pintura.color)
        
        for pintura in pinturas:
            
            dic = {
                "id": pintura.id,
                "nombre": pintura.nombre,
                "precio": pintura.precio,
                "color": pintura.color,
                "cantidad_pintura": pintura.cantidad_pintura,
                "cantidad": pintura.cantidad,
                "categoria": pintura.categoria,
                "subcategoria": pintura.subcategoria,
                "proveedor": pintura.categoria.prov_preferido,
                "estado": pintura.estado,
                "unidad_de_medida": pintura.unidad_de_medida,
                "ubicacion": pintura.ubicacion,
                "sucursal": pintura.sucursal,
                "stockminimo": pintura.stockminimo,
                "stockseguridad": pintura.stockseguridad,
                "colores": colores,
            }
            lista.append(dic)
    
    elif request.user.rol.opciones == 'VENDEDOR':
        
        vendedorQuery = Vendedor.objects.filter(id = request.user.id)
        cod = ""
        for vendedor in vendedorQuery:
            
            cod = vendedor.sucursal_id
            
        sucursalQuery = Sucursal.objects.filter(id = cod)
        
        sucursal = None
        for suc in sucursalQuery:
            sucursal = suc
        
        pinturas = Pintura.objects.filter(sucursal_id = sucursal.id)
        
        lista = []
        colores = []
        
        for pintura in pinturas:
            
            if pintura not in colores:
                
                colores.append(pintura.color)
        
        for pintura in pinturas:
            
            dic = {
                "id": pintura.id,
                "nombre": pintura.nombre,
                "precio": pintura.precio,
                "color": pintura.color,
                "cantidad_pintura": pintura.cantidad_pintura,
                "cantidad": pintura.cantidad,
                "categoria": pintura.categoria,
                "subcategoria": pintura.subcategoria,
                "proveedor": pintura.categoria.prov_preferido,
                "estado": pintura.estado,
                "unidad_de_medida": pintura.unidad_de_medida,
                "ubicacion": pintura.ubicacion,
                "sucursal": pintura.sucursal,
                "stockminimo": pintura.stockminimo,
                "stockseguridad": pintura.stockseguridad,
                "colores": colores,
            }
            lista.append(dic)
        
    elif request.user.rol.opciones == 'SUPERVISOR':
        
        supervisorQuery = Supervisor.objects.filter(id = request.user.id)
        cod = ""
        for supervisor in supervisorQuery:
            
            cod = supervisor.sucursal_id
            
        sucursalQuery = Sucursal.objects.filter(id = cod)
        
        sucursal = None
        for suc in sucursalQuery:
            sucursal = suc
        
        pinturas = Pintura.objects.filter(sucursal_id = sucursal.id)
        
        lista = []
        colores = []
        
        for pintura in pinturas:
            
            if pintura not in colores:
                
                colores.append(pintura.color)
        
        for pintura in pinturas:
            
            dic = {
                "id": pintura.id,
                "nombre": pintura.nombre,
                "precio": pintura.precio,
                "color": pintura.color,
                "cantidad_pintura": pintura.cantidad_pintura,
                "cantidad": pintura.cantidad,
                "categoria": pintura.categoria,
                "subcategoria": pintura.subcategoria,
                "proveedor": pintura.categoria.prov_preferido,
                "estado": pintura.estado,
                "unidad_de_medida": pintura.unidad_de_medida,
                "ubicacion": pintura.ubicacion,
                "sucursal": pintura.sucursal,
                "stockminimo": pintura.stockminimo,
                "stockseguridad": pintura.stockseguridad,
                "colores": colores,
            }
            lista.append(dic)

    return render(request, 'items/listar_pintura.html', locals())
    
    
    
    


class ListadoPinturaNueva(ValidarLoginYPermisosRequeridos, ListView):

    permission_required = ('item.view_pinturanueva',)
    model = PinturaNueva
    template_name = 'items/listar_pintura_nueva.html'
    queryset = PinturaNueva.objects.all().order_by('id')


class ListadoPinturaUsada(ValidarLoginYPermisosRequeridos, ListView):

    permission_required = ('item.view_pinturausada',)
    model = PinturaUsada
    template_name = 'items/listar_pintura_usada.html'
    queryset = PinturaUsada.objects.all().order_by('id')


class AgregarPintura(ValidarLoginYPermisosRequeridos, SuccessMessageMixin, CreateView):

    permission_required = ('item.view_pintura','item.add_pintura','item.change_pintura',)
    model = Pintura
    form_class = PinturaForm
    context_object_name = 'obj'
    template_name = 'items/crear_pintura.html'
    success_message = 'Pintura registrada con éxito.'
    success_url = reverse_lazy('items:listar_pinturas')
    
    def get_context_data(self, **kwargs):
        context = super(AgregarPintura, self).get_context_data(**kwargs)
        context["categoria"] = Categoria.objects.all()
        context["subcategoria"] = SubCategoria.objects.all()
        return context


class ListadoMezclas(ValidarLoginYPermisosRequeridos, ListView):

    permission_required = ('item.view_mezcla',)
    model = Mezcla
    template_name = 'items/listar_mezcla.html'
    queryset = Mezcla.objects.all().order_by('id')


class IniciarMezcla(ValidarLoginYPermisosRequeridos, SuccessMessageMixin, CreateView):

    permission_required = ('item.view_mezcla','item.add_mezcla', 'item.change_mezcla',)
    model = Mezcla
    form_class = MezclaForm
    template_name = 'items/iniciar_mezcla.html'
    success_message = 'Mezcla realizada correctamente.'
    success_url = reverse_lazy('items:listar_mezclas')


class ListadoMezclaUsada(ValidarLoginYPermisosRequeridos, ListView):

    permission_required = ('item.view_mezclausada',)
    model = MezclaUsada
    template_name = 'items/listar_mezcla_usada.html'
    queryset = MezclaUsada.objects.all().order_by('id')


class IniciarMezclaUsada(ValidarLoginYPermisosRequeridos, SuccessMessageMixin, CreateView):

    permission_required = ('item.view_mezclausada','item.add_mezclausada','item.change_mezclausada',)
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
    
    sucursalesIds = []

    rolesFromQuery = Rol.objects.filter(opciones='GERENTE GENERAL')
    rolId = ""
    for rol in rolesFromQuery:
        print(rol.id)
        rolId = rol.id

    es_gerente_general = request.user.rol_id == rolId
 
    
    sucursal_asociada = ""
    ItemFromQuery = Item.objects.all()
    
    if es_gerente_general or request.user.is_staff:
        es_gerente_general = True
        sucursalesQuery = Sucursal.objects.all()
        for sucursal in sucursalesQuery:
            sucursalesIds.append(sucursal.id)
    else:
        supervisorQuery = Supervisor.objects.filter(username = request.user.username)
        
        for supervisor in supervisorQuery:
            sucursal_asociada = supervisor.sucursal.id
        
        sucursalesIds.append(sucursal_asociada)

  
    
    lista = []
    for fila in ItemFromQuery:
        
       
        if fila.sucursal_id in sucursalesIds:
            lista.append(fila)
   
    
    items = []
    
    sucursales = []
    
    for item in lista:
        
        sucursalQuery = Sucursal.objects.filter(id = item.sucursal_id)
        for suc in sucursalQuery:
            if suc not in sucursales:
                sucursales.append(suc)

    for item in lista:
        dic = {
            
            "codigo_de_barras": item.codigo_de_barras,
            "nombre": item.nombre,
            "cantidad": item.cantidad,
            "stockminimo": item.stockminimo,
            "stockseguridad": item.stockseguridad,
            "es_gerente_general": str(es_gerente_general),
            "sucursales": sucursales,
            "sucursal_id": item.sucursal_id
        }

        items.append(dic)

    return render(request, 'items/reporte_riesgo_stock.html', locals())


def ReporteCambiosPrecios(request):
    filasReporte = []
    sucursalesIds = []
    supervisorBySucursal = {}

    rolesFromQuery = Rol.objects.filter(opciones='GERENTE GENERAL')
    rolId = ""
    for rol in rolesFromQuery:
        
        rolId = rol.id

    es_gerente_general = request.user.rol_id == rolId
    
    reportePreciosFromQuery = ReportePrecios.objects.all()
    for fila in reportePreciosFromQuery:
        supervisorBySucursal.setdefault(fila.responsable_usuario.id,fila.responsable)
   
    if es_gerente_general or request.user.is_staff:
        es_gerente_general = True
        sucursalesQuery = Sucursal.objects.all()
        for sucursal in sucursalesQuery:
            sucursalesIds.append(sucursal.id)
    else:
        for fila in reportePreciosFromQuery:
            # se supone que acá es el supervisor de la sucursal!!!
            
            
            sucursalesIds.append(supervisorBySucursal.get(request.user.id).sucursal_id)

    
    lista = []
    for fila in reportePreciosFromQuery:
        
        if fila.responsable.sucursal_id in sucursalesIds:
            lista.append(fila)
            
    sucursales = []
    
    for fila in lista:
        
        sucursalQuery = Sucursal.objects.filter(id = fila.responsable.sucursal_id)
        for suc in sucursalQuery:
            if suc not in sucursales:
                sucursales.append(suc)
    
    for fila in lista:
        
        dic = {
            "id": fila.id,
            "fecha": fila.fecha,
            "categoria": fila.categoria_asociada.opciones,
            "aumento": fila.aumento,
            "responsable": fila.responsable.nombre,
            "fecha_a_comparar": str(fila.fecha.date()),
            "es_gerente_general": str(es_gerente_general),
            "sucursales": sucursales,
            "responsable_sucursal": fila.responsable.sucursal_id
        }
        filasReporte.append(dic)

    return render(request, 'items/reporte_cambios_masivos.html', locals())

def ReporteCuentaCorrienteProveedores(request):
    
    sucursalesIds = []

    rolesFromQuery = Rol.objects.filter(opciones='GERENTE GENERAL')
    rolId = ""
    for rol in rolesFromQuery:
       
        rolId = rol.id

    es_gerente_general = request.user.rol_id == rolId
   
    
    sucursal_asociada = ""
    PedidosFromQuery = Pedidos.objects.all()
    
    if es_gerente_general or request.user.is_staff:
        es_gerente_general = True
        sucursalesQuery = Sucursal.objects.all()
        for sucursal in sucursalesQuery:
            sucursalesIds.append(sucursal.id)
    else:
        supervisorQuery = Supervisor.objects.filter(username = request.user.username)
        
        for supervisor in supervisorQuery:
            sucursal_asociada = supervisor.sucursal.id
        
        sucursalesIds.append(sucursal_asociada)

    
    
    lista = []
    for fila in PedidosFromQuery:
       
        if fila.sucursal_id in sucursalesIds:
            lista.append(fila)
   
    
    listaPedidos = []
    
    sucursales = []
    
    for pedido in lista:
        
        sucursalQuery = Sucursal.objects.filter(id = pedido.sucursal_id)
        for suc in sucursalQuery:
            if suc not in sucursales:
                sucursales.append(suc)
    

    for pedido in lista:
        dic = {
            "id": pedido.id,
            "cuenta_corriente_numero_cuenta": pedido.cuenta_corriente.numero_cuenta,
            "sucursal_codigo": pedido.sucursal.codigo,
            "proveedor_razon_social": pedido.proveedor.razon_social,
            "fecha": pedido.fecha,
            "total": pedido.total,
            "fecha_a_comparar": str(pedido.fecha.date()),
            "es_gerente_general": str(es_gerente_general),
            "sucursales": sucursales,
            "sucursal_id": pedido.sucursal_id
        }
        listaPedidos.append(dic)

    return render(request,'items/reporte_cuenta_corriente_proveedores.html',locals())

def HistorialPreferenciados(request, proveedor, categoria):
    
    query = HistorialPref.objects.filter(proveedor_asociado_id = proveedor, categoria_id = categoria).order_by('fecha')
    lista = []
    for info in query:
        lista.append(info)
        
    return render(request, 'items/historial_pref.html', locals())

def AsignarProveedor(request):
    
    if request.is_ajax():
        
        
        proveedor = request.POST.get('proveedor', None)
        categoria_id = request.POST.get('categoria', None)
        

        if int(proveedor) == 0:
            return HttpResponseBadRequest()
        else:
            hist_pref = HistorialPref()
            hist_pref.proveedor_asociado_id = int(proveedor)
            hist_pref.categoria_id = int(categoria_id)
            hist_pref.save()
            Categoria.objects.filter(id = int(categoria_id)).update(prov_preferido = int(proveedor))
            
    
    
    messages.success(request, 'Proveedor asignado correctamente.')
    return HttpResponse("")



def ordenarItemPorNombre(request):
    
    lista = []
    query = Item.objects.all().order_by('nombre')
    
    for info in query:
        
        lista.append(info)
    
    return render(request, 'items/listar_item_nombre.html', locals())

def ordenarPorStockMinimo(request):
    
    lista = []
    query = Item.objects.all().order_by('stockminimo','cantidad')
    
    for info in query:
        
        lista.append(info)
    
    return render(request, 'items/listar_item_stockminimo.html', locals())

def ordenarPorStockSeguridad(request):
    
    lista = []
    query = Item.objects.all().order_by('stockseguridad','cantidad')
    
    for info in query:
        
        lista.append(info)
    
    return render(request, 'items/listar_item_stockseguridad.html', locals())


def RealizarPedido(request, item):
    
    if request.is_ajax():
        
        cantidad = request.POST.get('cantidad_ingresada', None)
        item = request.POST.get('item', None)
        
        
        if cantidad == "":
            messages.error(request, "Sólo puedes ingresar una cantidad mayor o igual a 0.")
            return HttpResponse()
        if int(cantidad) <= 0:
            messages.error(request, "No puedes ingresar digitos negativos.")
            return HttpResponse()
        
        items = Item.objects.filter(id = int(item))
        pedido_id = 0

        for item in items:
            cuentas = CuentaCorrienteProveedor.objects.filter(proveedor = item.categoria.prov_preferido)
            cuenta_corriente = 0
            
            for cuenta in cuentas:
                cuenta_corriente = cuenta.numero_cuenta
            
            if item.solicitud == False:
                item.solicitud = True
                item.reintentos = 0
                item.save()
                pedido = Pedidos()
                pedido.item = item
                pedido.sucursal = item.sucursal
                pedido.solicitado = int(cantidad)
                pedido.proveedor = item.categoria.prov_preferido
                pedido.cuenta_corriente_id = cuenta_corriente
        
                if item.repo_por_lote:
                    pedido.cantidad = item.cantidad_lote * 2
                pedido.save()
                pedido_id = pedido.id
            item.reintentos = 0
            item.save()

        
        pedidos = Pedidos.objects.filter(id = pedido_id)       

        for pedido in pedidos:
            emailProv = Proveedor.objects.filter(id = pedido.proveedor_id)
            email = ""
            for info in emailProv:
                email = info.email
                
            try:
                send_mail('SOLICITUD DE STOCK - SUCURSAL ' + str(pedido.sucursal_id), "Buenas tardes, esta es una solicitud de stock automática. Por favor, diríjase al siguiente link para indicar las cantidades que nos puede proveer de cada ítem:\n" +
                            "https://prismatechnology.herokuapp.com/items/pedido_proveedor/" + str(pedido.proveedor_id) + "/" + str(pedido.sucursal_id), 'tmmzprueba@gmail.com', {email})
                
            except:
                
                return HttpResponseBadRequest()
    messages.success(request, "Solicitud de stock enviada correctamente.")
    return HttpResponse()


def SolicitarStock(request, item):
    
    lista = []
    
    ItemQuery = Item.objects.filter(id = item)
    item = None
    for item in ItemQuery:
        item = item
    
    if item.sucursal.estado.opciones == 'INACTIVA':
        messages.warning(request, "La sucursal del item seleccionado se encuentra inactiva.")
        return redirect('items:listar_items')
    
    if item.categoria.prov_preferido == None:
        messages.warning(request, "Debes asignar un proveedor preferido a la categoria que pertenece el item.")
        return redirect('items:listar_items')
    
    if item.estado.opciones == 'INACTIVO':
        messages.warning(request, "No puedes solicitar stock de un item inactivo.")
        return redirect('items:listar_items')
    
    sucursales = Sucursal.objects.filter(id = item.sucursal_id)
    sucursal = 0
    nombre = ""
    for suc in sucursales:
        sucursal = suc.id
        nombre = suc.codigo
        
    supervisor = Supervisor.objects.filter(sucursal_id = sucursal)
    
    if len(supervisor) == 0:
        messages.warning(request, "Debes asignar un supervisor para la sucursal "+ nombre + " para poder realizar ésta acción.")
        return redirect('items:listar_items')
    
    for item in ItemQuery:
        
        lista.append(item)
    
    return render(request, 'items/solicitar_stock.html', locals())


def ReporteItemsStockFaltante(request):
    sucursalesIds = []

    rolesFromQuery = Rol.objects.filter(opciones='GERENTE GENERAL')
    rolId = ""
    for rol in rolesFromQuery:
      
        rolId = rol.id

    es_gerente_general = request.user.rol_id == rolId
   

    sucursal_asociada = ""
    estadosQuery = Estado.objects.filter(opciones = 'ACTIVO')

    estadoId = ""
    for estado in estadosQuery:
        estadoId = estado.id

    ItemFromQuery = Item.objects.filter(cantidad = 0, estado = estadoId)

    if es_gerente_general or request.user.is_staff:
        es_gerente_general = True
        sucursalesQuery = Sucursal.objects.all()
        for sucursal in sucursalesQuery:
            sucursalesIds.append(sucursal.id)
    else:
        supervisorQuery = Supervisor.objects.filter(username = request.user.username)

        for supervisor in supervisorQuery:
            sucursal_asociada = supervisor.sucursal.id

        sucursalesIds.append(sucursal_asociada)

   

    lista = []
    for fila in ItemFromQuery:
      
        if fila.sucursal_id in sucursalesIds:
            lista.append(fila)
    

    items = []
    
    sucursales = []
    
    for item in lista:
        
        sucursalQuery = Sucursal.objects.filter(id = item.sucursal_id)
        for suc in sucursalQuery:
            if suc not in sucursales:
                sucursales.append(suc)

    for item in lista:
        dic = {
            "codigo_de_barras": item.codigo_de_barras,
            "nombre": item.nombre,
            "cantidad": item.cantidad,
            "stockminimo": item.stockminimo,
            "stockseguridad": item.stockseguridad,
            "es_gerente_general": str(es_gerente_general),
            "sucursales": sucursales,
            "sucursal_id": item.sucursal_id,
            "sucursal": item.sucursal,
            "precio": item.precio,
            "categoria": item.categoria,
            "subcategoria": item.subcategoria,
            "categoria_prov_preferido": item.categoria.prov_preferido,
            "estado": item.estado,
            "ubicacion": item.ubicacion
        }
        items.append(dic)

    return render(request,'items/reporte_stock_faltante.html',locals())


