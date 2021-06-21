from email.mime.nonmultipart import MIMENonMultipart
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.views.generic.edit import UpdateView
from .forms import VentaLocalForm
from .models import ComprobantePago, EstadoVenta, VentaLocal, VentaVirtual, Venta, ItemVenta, Cotizacion
from django.views.generic import  CreateView,  DeleteView, ListView
from usuario.mixins import ValidarLoginYPermisosRequeridos
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import ProtectedError
from cliente.models import Cliente, CuentaCorriente,MedioDePago, Deuda, EstadoDeuda, CategoriaCliente, TipoDeMoneda
from sucursal.models import Sucursal, Caja, Operacion
from usuario.models import Vendedor
from item.models import Item, Estado
from django.http import HttpResponse, HttpResponseBadRequest
from decimal import Decimal
import json
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import EmailMultiAlternatives
from usuario.models import Supervisor, Rol
from django.db.models import Count





class ListadoVenta(ValidarLoginYPermisosRequeridos,ListView):
    
    permission_required = ('venta.view_venta',)
    model = Venta
    template_name = 'ventas/listar_venta.html'
    queryset = Venta.objects.all().order_by('numero_comprobante').order_by('fecha').order_by('sucursal_asociada')

class ListadoVentaCajero(ValidarLoginYPermisosRequeridos,ListView):
    
    permission_required = ('venta.view_ventavirtual','venta.add_ventavirtual',)
    model = Venta 
    template_name = 'ventas/listar_venta_cajero.html'
    queryset = Venta.objects.all().order_by('numero_comprobante')

class RegistrarVentaLocal(ValidarLoginYPermisosRequeridos,SuccessMessageMixin,CreateView):
    
    permission_required = ('venta.view_venta','venta.add_venta',)
    model = VentaLocal
    context_object_name = 'obj'
    form_class = VentaLocalForm
    template_name = 'ventas/crear_venta_local.html'
    success_url = reverse_lazy('ventas:listar_ventas')
    success_message = 'Venta local registrada correctamente.'
      
    
    def get_context_data(self, **kwargs):
        context = super(RegistrarVentaLocal, self).get_context_data(**kwargs)
        context["cliente_asociado"] = Cliente.objects.all()
        context["mediodepago"] = MedioDePago.objects.all()
        context["cuenta_corriente"] = CuentaCorriente.objects.all()
        context["sucursal_asociada"] = Sucursal.objects.all()
        context["vendedor_asociado"] = Vendedor.objects.all()
        return context
    
    
    
    
class EditarVentaLocal(ValidarLoginYPermisosRequeridos,SuccessMessageMixin, UpdateView):
    
    permission_required = ('venta.view_venta','venta.add_venta',)
    model = VentaLocal
    fields = ['monto_ingresado']
    template_name = 'ventas/editar_venta.html'
    success_url = reverse_lazy('ventas:listar_ventas')
    success_message = 'Monto ingresado correctamente.'
    
# class EliminarVenta(ValidarLoginYPermisosRequeridos,SuccessMessageMixin,DeleteView):
    
#     permission_required = ('venta.view_venta','venta.delete_venta',)
#     model = Venta
#     template_name = 'ventas/eliminar_venta.html'
#     success_url = reverse_lazy('ventas:listar_ventas')
#     success_message = 'Se eliminó la venta correctamente.'
                                    
#     def delete(self, request, *args, **kwargs):
        
#         self.object = self.get_object()
#         success_url = self.get_success_url()

#         try:
#             self.object.delete()
#         except ProtectedError:
#             messages.add_message(request, messages.ERROR, 'No se puede eliminar: Ésta venta está relacionada.')
#             return redirect('ventas:listar_ventas')

#         return HttpResponseRedirect(success_url)                                
    
    

def ListarItem(request, venta):
    
    
    items = ItemVenta.objects.filter(venta_asociada = venta)
   
    lista = []
    for item in items:
        
        lista.append(item)
   
    return render(request, 'ventas/listar_itemventa.html', locals())

def VerItems(request, venta):
    
    
    items = ItemVenta.objects.filter(venta_asociada = venta)
   
    lista = []
    for item in items:
        
        lista.append(item)
   
    return render(request, 'ventas/ver_items.html', locals())
        
        
def VerDetalle(request, sucursal, venta):
    
   
    sucursal = Sucursal.objects.get(id = sucursal)
    estados = Estado.objects.filter(opciones = 'ACTIVO')
    nuevo_estado = 0
    for estado in estados:
        nuevo_estado = estado.id
    
    queryset = Item.objects.filter(sucursal = sucursal.id, estado = nuevo_estado)
    lista = []
    for item in queryset:
        dic = {
            "nombre": item.nombre,
            "categoria": item.categoria,
            "precio": item.precio,
            "estado": item.estado,
            "unidad": item.unidad_de_medida,
            "ubicacion": item.ubicacion,
            "id": item.id,
            "sucursal": item.sucursal,
            "venta": venta,
            
        }
        lista.append(dic)
         
   
    
    return render(request, 'ventas/crear_itemventa.html',locals())


def AgregarItem(request, sucursal, venta):
    
    
    if request.is_ajax():
        object = json.loads(request.POST.get('items'))
        
        lista_items = []
        lista_ventas = []
        lista_errores = []
        lista_success = []
        contador = 0
        
        for info in object:
            objeto = json.loads(info)
            
            item = objeto['item']
            cantidad = objeto['cantidad']
            sucursal = objeto['sucursal']
            venta = objeto['venta']
            precio = objeto['precio']
            
            item_venta = ItemVenta()
            item_venta.item_id = int(item)
        
            if cantidad.isdigit():
                item_venta.cantidad_solicitada = int(cantidad)
            else:
                return HttpResponseBadRequest()
    
                
            item_venta.sucursal_asociada_id = str(sucursal)
            item_venta.venta_asociada_id = int(venta)
            item_venta.monto = Decimal(cantidad.replace(',', '.')) * Decimal(precio.replace(',', '.'))
            
            
            
            validacion = validar(request, item_venta)
            
            if validacion != None:
                
                lista_errores.append(validacion)
                continue
            else:
                lista_success.append(item_venta.item.nombre)
            
            lista_items.append(item_venta.item_id)
            lista_ventas.append(item_venta.venta_asociada_id)
            
            item_venta.save()
            
            queryset = Venta.objects.raw("""
                SELECT * 
                FROM venta_venta
                WHERE numero_comprobante IN %s               
            """, [tuple(lista_ventas)])  
            
            tipodemoneda1 = TipoDeMoneda.objects.filter(opciones = 'EURO')
            tipoeuro = 0
            valor_euro = ""
            
            for tipo in tipodemoneda1:
                tipoeuro = tipo.id  
            euro = Cotizacion.objects.filter(moneda = tipoeuro)
            for e in euro:
                valor_euro = e.cotizacion 
            
            tipodemoneda2 = TipoDeMoneda.objects.filter(opciones = 'DOLAR')
            tipodolar = 0
            valor_dolar = ""
            
            for tipo in tipodemoneda2:
                tipodolar = tipo.id  
            dolar = Cotizacion.objects.filter(moneda = tipodolar)
            for d in dolar:
                valor_dolar = d.cotizacion  
            
            
            for venta in queryset:
                
                if venta.tipo_de_moneda.opciones == 'EURO':
                    
                    venta.total_euro += (item_venta.monto / valor_euro)
                    
                
                elif venta.tipo_de_moneda.opciones == 'DOLAR':
                    venta.total_dolar += (item_venta.monto / valor_dolar)
                    
                else:
                    venta.total_peso += item_venta.monto
                    
                venta.save()
        
        
            if len(lista_items) > 0:
                item_de_venta = Item.objects.raw("""
                    SELECT * 
                    FROM item_item 
                    WHERE id IN %s               
                """, [tuple(lista_items)])  
                
                contador = 0
                
                for item in item_de_venta:
                    
                    if (item.cantidad - item_venta.cantidad_solicitada) < 0:
                        return HttpResponseBadRequest()
                    else:
                        contador += 1
                        if contador == 1:
                            item.cantidad -= item_venta.cantidad_solicitada
                            item.save() 
                
            
        mensaje = "Se añadieron: "
        for m in lista_success:
            mensaje += m + ", "
        if len(lista_success) == 0:    
            mensaje = "No se añadieron: "
        else:
            mensaje = mensaje[0:len(mensaje)-2] + ".\nNo se añadieron: "
            
        for m in lista_errores:
            mensaje += m + ", "
        
        if len(lista_errores) == 0:
            mensaje = mensaje[0:len(mensaje)-18] 
        else:
            mensaje = mensaje[0:len(mensaje)-2] + "."
        print(lista_success)
        print(lista_errores)
        #messages.success(request, "Item agregado correctamente.")
        return HttpResponse(mensaje)
    

def validar(request, item_venta):
    
    if item_venta.item.cantidad == 0:
        #messages.error(request, "No hay stock del item solicitado.")
        return item_venta.item.nombre + " (No hay stock del item solicitado)"
        
        
    if item_venta.venta_asociada.cliente_asociado.nombre == 'CONSUMIDOR FINAL' and item_venta.item.precio >= 10000:
        
         #messages.error(request, "Es necesario registrar al cliente para agregar el item.")
         return item_venta.item.nombre + " (Es necesario registrar al cliente para agregar el item)"
    
    
    if item_venta.item.cantidad < item_venta.cantidad_solicitada:
        #messages.error(request,"No disponemos de la cantidad solicitada. Stock actual: " + str(item_venta.item.cantidad))
        return item_venta.item.nombre + " (No disponemos de la cantidad solicitada. Stock actual: " + str(item_venta.item.cantidad) + ")"
    
    
    if item_venta.cantidad_solicitada < 0:
        #messages.error(request,"La cantidad no puede ser negativa.") 
        return item_venta.item.nombre + " (La cantidad no puede ser negativa)"
    
    if item_venta.cantidad_solicitada == 0:
        return item_venta.item.nombre + " (Debe seleccionar una cantidad)"


def AnularVenta(request, venta):
    
    ventas = Venta.objects.filter(numero_comprobante = venta)
    venta = None
    for ven in ventas:
        venta = ven
    estados = EstadoVenta.objects.filter(opciones = 'RECHAZADA')
    items = ItemVenta.objects.filter(venta_asociada_id =venta.numero_comprobante)
    rechazada = ""
    for estado in estados:
        rechazada = estado.id
        
    if venta.estado.opciones == 'EN PREPARACION':
        if len(items) == 0:
            try:
                
                venta.estado_id = rechazada
                venta.save()
                messages.success(request, "Venta anulada.")
                print("hola")
                return redirect('ventas:listar_ventas')
                
                
            except:
                
                messages.error(request, "¡Verifica los datos!, no se ha podido anular la venta.")
                return redirect('ventas:listar_ventas')
        else:
            messages.error(request, "Debes eliminar los items agregados para anular la venta.")
            return redirect('ventas:listar_ventas')
                
    elif venta.estado.opciones == 'RECHAZADA':
        messages.info(request, "La venta ya se encuentra anulada.")
    
    else:
        messages.warning(request, "Sólo puedes anular ventas que se encuentren EN PREPARACIÓN.")
        
    return redirect('ventas:listar_ventas')


def CambiarEstado(request, id, cliente):

    queryset = Venta.objects.filter(numero_comprobante = id)
    queryset1 = EstadoVenta.objects.filter(opciones = 'LISTA')
    nuevo_estado = ""
    instancia = None
    deuda = Deuda.objects.filter(cliente_asociado_id = cliente, numero_venta = id)
    en_deuda = EstadoVenta.objects.filter(opciones = 'EN DEUDA')
    tipodemoneda1 = TipoDeMoneda.objects.filter(opciones = 'EURO')
    tipoeuro = 0
    valor_euro = ""
    
    
    for tipo in tipodemoneda1:
        tipoeuro = tipo.id  
    euro = Cotizacion.objects.filter(moneda = tipoeuro)
    for e in euro:
        valor_euro = e.cotizacion 
    
    tipodemoneda2 = TipoDeMoneda.objects.filter(opciones = 'DOLAR')
    tipodolar = 0
    valor_dolar = ""
    
    for tipo in tipodemoneda2:
        tipodolar = tipo.id  
    dolar = Cotizacion.objects.filter(moneda = tipodolar)
    for d in dolar:
        valor_dolar = d.cotizacion 
        
    for est in queryset1:
        nuevo_estado = est.id

    for venta in queryset:
        instancia = venta
        
        if instancia.tipo_de_moneda.opciones == 'EURO':
            if instancia.total_euro >= (10000 / valor_euro) and instancia.cliente_asociado.nombre == 'CONSUMIDOR FINAL':
                messages.error(request, "Es necesario registrar al cliente para agregar el item")
                return redirect('ventas:listar_ventas')
            # if instancia.vendedor_asociado.id != request.user.id:
            #     messages.error(request, "No puedes cargar una venta de otra sucursal.")
            #     return redirect('ventas:listar_ventas')
            if instancia.total_euro == 0:
                messages.error(request, 'No puedes cargar una venta sin items.')
                return redirect('ventas:listar_ventas')
            
            if instancia.monto_ingresado <= 0:
                messages.error(request, 'Debes ingresar el monto del cliente.')
                return redirect('ventas:listar_ventas')
            
            if instancia.monto_ingresado < instancia.total_euro and instancia.cliente_asociado.nombre == 'CONSUMIDOR FINAL':
                messages.error(request, 'El consumidor final debe abonar el total de la venta.')
                return redirect('ventas:listar_ventas')
            
            elif instancia.monto_ingresado < instancia.total_euro and len(deuda) == 0:
                estado_deuda = EstadoDeuda.objects.filter(opciones = 'IMPAGA')
                
                nuevo_estado= ""
                for est in estado_deuda:
                    nuevo_estado = est.id
                deuda = Deuda()
                deuda.monto = instancia.total_euro - instancia.monto_ingresado
                deuda.estado_deuda_id = nuevo_estado
                deuda.cliente_asociado_id = cliente
                deuda.numero_venta = id
                deuda.save()
                
                for estado in en_deuda:
                    venta.estado_id = estado.id
                    venta.save()
                    messages.success(request, "Venta en estado de deuda.")
                    return redirect('ventas:listar_ventas')
            
            elif instancia.monto_ingresado < instancia.total_euro and len(deuda) > 0:
                
                # cliente = Cliente.objects.filter(id = cliente)
                # categorias = CategoriaCliente.objects.filter(opciones = 'B')
                # categoria_b = ""
                # for categoria in categorias:
                #     categoria_b = categoria.id
                # for cli in cliente:
                #     cli.categoria_cliente = categoria_b
                #     cli.save()
                
                for d in deuda:
                    
                    d.monto = instancia.total_euro - instancia.monto_ingresado
                    d.save()
                    
                for estado in en_deuda:
                    venta.estado_id = estado.id
                    venta.save()
                    messages.success(request, "Monto insuficiente para cargar la venta.")
                    return redirect('ventas:listar_ventas')
            else:
                venta.estado_id = nuevo_estado
                venta.save()
                Deuda.objects.filter(cliente_asociado_id = cliente, numero_venta = id).delete()
                messages.success(request, "Venta lista para su ejecución.")
                return redirect('ventas:listar_ventas')
        
        elif instancia.tipo_de_moneda.opciones == 'DOLAR':
            if instancia.total_dolar >= (10000 / valor_dolar) and instancia.cliente_asociado.nombre == 'CONSUMIDOR FINAL':
                messages.error(request, "Es necesario registrar al cliente para agregar el item")
                return redirect('ventas:listar_ventas')
            # if instancia.vendedor_asociado.id != request.user.id:
            #     messages.error(request, "No puedes cargar una venta de otra sucursal.")
            #     return redirect('ventas:listar_ventas')
            if instancia.total_dolar == 0:
                messages.error(request, 'No puedes cargar una venta sin items.')
                return redirect('ventas:listar_ventas')
            
            if instancia.monto_ingresado <= 0:
                messages.error(request, 'Debes ingresar el monto del cliente.')
                return redirect('ventas:listar_ventas')
            
            elif instancia.monto_ingresado < instancia.total_dolar and len(deuda) == 0:
                estado_deuda = EstadoDeuda.objects.filter(opciones = 'IMPAGA')
                
                nuevo_estado= ""
                for est in estado_deuda:
                    nuevo_estado = est.id
                deuda = Deuda()
                deuda.monto = instancia.total_dolar - instancia.monto_ingresado
                deuda.estado_deuda_id = nuevo_estado
                deuda.cliente_asociado_id = cliente
                deuda.numero_venta = id
                deuda.save()
                
                for estado in en_deuda:
                    venta.estado_id = estado.id
                    venta.save()
                    messages.success(request, "Venta en estado de deuda.")
                    return redirect('ventas:listar_ventas')
            
            elif instancia.monto_ingresado < instancia.total_dolar and len(deuda) > 0:
                
                # cliente = Cliente.objects.filter(id = cliente)
                # categorias = CategoriaCliente.objects.filter(opciones = 'B')
                # categoria_b = ""
                # for categoria in categorias:
                #     categoria_b = categoria.id
                # for cli in cliente:
                #     cli.categoria_cliente = categoria_b
                #     cli.save()
                
                for d in deuda:
                    
                    d.monto = instancia.total_dolar - instancia.monto_ingresado
                    d.save()
                    
                for estado in en_deuda:
                    venta.estado_id = estado.id
                    venta.save()
                    messages.success(request, "Monto insuficiente para cargar la venta.")
                    return redirect('ventas:listar_ventas')
            else:
                venta.estado_id = nuevo_estado
                venta.save()
                Deuda.objects.filter(cliente_asociado_id = cliente, numero_venta = id).delete()
                messages.success(request, "Venta lista para su ejecución.")
                return redirect('ventas:listar_ventas')
        else:
            if instancia.total_peso >= 10000 and instancia.cliente_asociado.nombre == 'CONSUMIDOR FINAL':
                messages.error(request, "Es necesario registrar al cliente para agregar el item")
                return redirect('ventas:listar_ventas')
            # if instancia.vendedor_asociado.id != request.user.id:
            #     messages.error(request, "No puedes cargar una venta de otra sucursal.")
            #     return redirect('ventas:listar_ventas')
            if instancia.total_peso == 0:
                messages.error(request, 'No puedes cargar una venta sin items.')
                return redirect('ventas:listar_ventas')
            
            if instancia.monto_ingresado <= 0:
                messages.error(request, 'Debes ingresar el monto del cliente.')
                return redirect('ventas:listar_ventas')
            
            elif instancia.monto_ingresado < instancia.total_peso and len(deuda) == 0:
                estado_deuda = EstadoDeuda.objects.filter(opciones = 'IMPAGA')
                
                nuevo_estado= ""
                for est in estado_deuda:
                    nuevo_estado = est.id
                deuda = Deuda()
                deuda.monto = instancia.total_peso - instancia.monto_ingresado
                deuda.estado_deuda_id = nuevo_estado
                deuda.cliente_asociado_id = cliente
                deuda.numero_venta = id
                deuda.save()
                
                for estado in en_deuda:
                    venta.estado_id = estado.id
                    venta.save()
                    messages.success(request, "Venta en estado de deuda.")
                    return redirect('ventas:listar_ventas')
            
            elif instancia.monto_ingresado < instancia.total_peso and len(deuda) > 0:
                
                # cliente = Cliente.objects.filter(id = cliente)
                # categorias = CategoriaCliente.objects.filter(opciones = 'B')
                # categoria_b = ""
                # for categoria in categorias:
                #     categoria_b = categoria.id
                # for cli in cliente:
                #     cli.categoria_cliente = categoria_b
                #     cli.save()
                
                for d in deuda:
                    
                    d.monto = instancia.total_peso - instancia.monto_ingresado
                    d.save()
                    
                for estado in en_deuda:
                    venta.estado_id = estado.id
                    venta.save()
                    messages.success(request, "Monto insuficiente para cargar la venta.")
                    return redirect('ventas:listar_ventas')
            else:
                venta.estado_id = nuevo_estado
                venta.save()
                Deuda.objects.filter(cliente_asociado_id = cliente, numero_venta = id).delete()
                messages.success(request, "Venta lista para su ejecución.")
                return redirect('ventas:listar_ventas')
    


def eliminarItem(request, venta, item):
    
    item_venta = ItemVenta.objects.filter(venta_asociada = venta, id = item)
    
    item_asociado = 0
    venta_asociada = 0
    cantidad_solicitada = 0
    monto = 0
    
    for item in item_venta:
        item_asociado = item.item_id 
        venta_asociada = item.venta_asociada_id   
        cantidad_solicitada = item.cantidad_solicitada
        monto = item.monto
        
    
    item_de_venta = Item.objects.filter(id = item_asociado)  
   
    for item in item_de_venta:
        
        item.cantidad += cantidad_solicitada
        item.save() 
        
    queryset = Venta.objects.filter(numero_comprobante = venta_asociada)
    tipodemoneda1 = TipoDeMoneda.objects.filter(opciones = 'EURO')
    tipoeuro = 0
    valor_euro = ""
    
    for tipo in tipodemoneda1:
        tipoeuro = tipo.id  
    euro = Cotizacion.objects.filter(moneda = tipoeuro)
    for e in euro:
        valor_euro = e.cotizacion 
    
    tipodemoneda2 = TipoDeMoneda.objects.filter(opciones = 'DOLAR')
    tipodolar = 0
    valor_dolar = ""
    
    for tipo in tipodemoneda2:
        tipodolar = tipo.id  
    dolar = Cotizacion.objects.filter(moneda = tipodolar)
    for d in dolar:
        valor_dolar = d.cotizacion 
        
    for venta in queryset:
        
        if venta.tipo_de_moneda.opciones == 'EURO':      
            venta.total_euro -= (monto / valor_euro)
        
        elif venta.tipo_de_moneda.opciones == 'DOLAR':
            venta.total_dolar -= (monto / valor_dolar)
            
        else:
            venta.total_peso -= monto
            
        venta.save()
        
    item_venta.delete()
    
    messages.success(request, "Se ha quitado el item de la venta.")
    return redirect('ventas:listar_ventas')

def eliminarItemCajero(request, venta, item):
    
    item_venta = ItemVenta.objects.filter(venta_asociada = venta, id = item)
    
    item_asociado = 0
    venta_asociada = 0
    cantidad_solicitada = 0
    monto = 0
    
    for item in item_venta:
        item_asociado = item.item_id 
        venta_asociada = item.venta_asociada_id   
        cantidad_solicitada = item.cantidad_solicitada
        monto = item.monto
        
    
    item_de_venta = Item.objects.filter(id = item_asociado)  
   
    for item in item_de_venta:
        
        item.cantidad += cantidad_solicitada
        item.save() 
        
    queryset = Venta.objects.filter(numero_comprobante = venta_asociada)
    tipodemoneda1 = TipoDeMoneda.objects.filter(opciones = 'EURO')
    tipoeuro = 0
    valor_euro = ""
    
    for tipo in tipodemoneda1:
        tipoeuro = tipo.id  
    euro = Cotizacion.objects.filter(moneda = tipoeuro)
    for e in euro:
        valor_euro = e.cotizacion 
    
    tipodemoneda2 = TipoDeMoneda.objects.filter(opciones = 'DOLAR')
    tipodolar = 0
    valor_dolar = ""
    
    for tipo in tipodemoneda2:
        tipodolar = tipo.id  
    dolar = Cotizacion.objects.filter(moneda = tipodolar)
    for d in dolar:
        valor_dolar = d.cotizacion 
        
    for venta in queryset:
        
        if venta.tipo_de_moneda.opciones == 'EURO':      
            venta.total_euro -= (monto / valor_euro)
        
        elif venta.tipo_de_moneda.opciones == 'DOLAR':
            venta.total_dolar -= (monto / valor_dolar)
            
        else:
            venta.total_peso -= monto
            
        venta.save()
        
    item_venta.delete()
    
    messages.error(request, "Se ha quitado el item de la venta.")
    return redirect('ventas:listar_ventas_cajero')

def FinalizarVenta(request, venta):
    
    venta_obtenida = Venta.objects.filter(numero_comprobante = venta)
    instancia = None
    sucursal_asociada = 0
    total = 0
    
        
    for venta in venta_obtenida:
        
       
        instancia = venta
        sucursal_asociada = venta.sucursal_asociada
        cajas = Caja.objects.filter(sucursal_id = sucursal_asociada.id)
    
        if len(cajas) == 0:
            messages.error(request, "Debes registrar una caja para la sucursal seleccionada.")
            return redirect('ventas:listar_ventas_cajero')
        
        if venta.tipo_de_moneda.opciones == 'EURO':
            if venta.total_euro <= 0:
                messages.error(request, "No es posible realizar una venta sin agregar items.")
                return redirect('ventas:listar_ventas_cajero')      
            total = venta.total_euro
        
        elif venta.tipo_de_moneda.opciones == 'DOLAR':
            if venta.total_dolar <= 0:
                messages.error(request, "No es posible realizar una venta sin agregar items.")
                return redirect('ventas:listar_ventas_cajero')
            total = venta.total_dolar
            
        else:
            if venta.total_peso <= 0:
                messages.error(request, "No es posible realizar una venta sin agregar items.")
                return redirect('ventas:listar_ventas_cajero')
            total = venta.total_peso
        
        
    cajas = Caja.objects.filter(sucursal_id = sucursal_asociada.id)
    
    
    caja_menor = None
    monto = total
    
    for caja in cajas:
        
        if instancia.tipo_de_moneda.opciones == 'EURO':  
            if caja.saldo_disponible_euros < monto:
                monto = caja.saldo_disponible_euros
                caja_menor = caja
            else:
                caja_menor = caja
        elif instancia.tipo_de_moneda.opciones == 'DOLAR':
            if caja.saldo_disponible_dolares < monto:
                monto = caja.saldo_disponible_dolares
                caja_menor = caja
            else:
                caja_menor = caja
        else:
            if caja.saldo_disponible < monto:
                monto = caja.saldo_disponible
                caja_menor = caja
            else:
                caja_menor = caja
    
    
    if instancia.tipo_de_moneda.opciones == 'EURO':
        caja_menor.saldo_disponible_euros = caja_menor.saldo_disponible_euros + total
        if (total * Decimal("115.21".replace(',', '.'))) >= 20000 and instancia.mediodepago.opciones == 'EFECTIVO':
            caja_menor.ingresos_en_euros += total - (total * Decimal("0.05".replace(',', '.')))
            total -= (total * Decimal("0.05".replace(',', '.')))
        else:
            caja_menor.ingresos_en_euros += total
        
    elif instancia.tipo_de_moneda.opciones == 'DOLAR':
        caja_menor.saldo_disponible_dolares = caja_menor.saldo_disponible_dolares + total
        if (total * Decimal("95.18".replace(',', '.'))) >= 20000 and instancia.mediodepago.opciones == 'EFECTIVO':
            caja_menor.ingresos_en_dolares += total - (total * Decimal("0.05".replace(',', '.')))
            total -= (total * Decimal("0.05".replace(',', '.')))
        else:
            caja_menor.ingresos_en_dolares += total
            
    else:
        caja_menor.saldo_disponible = caja_menor.saldo_disponible + total
        if total >= 20000 and instancia.mediodepago.opciones == 'EFECTIVO':
            caja_menor.ingresos_en_pesos += total - (total * Decimal("0.05".replace(',', '.')))
            total -= (total * Decimal("0.05".replace(',', '.')))
        else:
            caja_menor.ingresos_en_pesos += total
    caja_menor.save()
    
    ids = EstadoVenta.objects.filter(opciones = 'PAGADA')
    nuevo_estado = ""
    for id in ids:
        nuevo_estado = id.id
        
    instancia.estado_id = nuevo_estado
    instancia.save()
    movimiento = Operacion()
    movimiento.monto = "+" + str(total) + " (En "+ instancia.tipo_de_moneda.opciones + ")"
    movimiento.tipo = "Venta"
    movimiento.caja_asociada = caja_menor
    movimiento.identificador = "N° de comprobante " + str(instancia.numero_comprobante)
    movimiento.responsable = request.user.id
    movimiento.save()
    
    comprobante_de_pago = ComprobantePago()
    comprobante_de_pago.numero_venta = instancia.numero_comprobante
    comprobante_de_pago.mediodepago = instancia.mediodepago.opciones
    comprobante_de_pago.moneda = instancia.tipo_de_moneda.opciones
    comprobante_de_pago.vendedor = instancia.vendedor_asociado.nombre
    comprobante_de_pago.sucursal = instancia.sucursal_asociada.codigo
    comprobante_de_pago.total = "$ " + str(round(total, 2))
    comprobante_de_pago.save()
    
    querycliente = Cliente.objects.filter(id = instancia.cliente_asociado_id)
    cliente = ""
    for cliente in querycliente:
        cliente = cliente
    
    
    # email = EmailMessage("Venta realizada - Prisma Technology",
    #                              "Hola {}.\n\n {} ".format(cliente.nombre,"Felicidades, te queremos informar que la venta ha sido procesada y se encuentra pagada.\n Gracias por confiar en nosotros.\n [Aquí estaría el comprobante de pago - SPRINT 4]" ),
    #                              "",[cliente.email], reply_to=["VENTA REALIZADA"])
    
    subject, from_email, to = 'Venta realizada - Prisma Technology ', 'tmmzprueba@gmail.com', cliente.email
    text_content = 'Felicidades, te queremos informar que la venta ha sido procesada y se encuentra pagada.\n Gracias por confiar en nosotros.'
    html_content = '<div id="comprobante" class="text-center"> <p>' + text_content + '</p><br><p><b> Comprobante de pago: </b> </p><br> <ul> <li> N° de venta: ' + str(comprobante_de_pago.numero_venta) + '</li><li> Medio de pago: ' + comprobante_de_pago.mediodepago + '</li><li> Moneda: ' + comprobante_de_pago.moneda + '</li><li> Vendedor Asignado: '+ comprobante_de_pago.vendedor + '</li><li> Sucursal Asignada: ' + comprobante_de_pago.sucursal +'</li><li> Total: '+ comprobante_de_pago.total + '</li></ul>' 
   
    email = EmailMultiAlternatives(subject, text_content, from_email, [to])
    email.attach_alternative(html_content, "text/html")
    
    # urllib.request.urlretrieve(
    # 'https://image.pngaaa.com/426/34426-middle.png',
    # "comprobantes/doge.png")
  
    # img = Image.open("comprobantes/doge.png")
    
    # email.attach_file(img.filename)
    
    try:
        email.send()
    except:
        
        messages.error(request, 'Ocurrió un error al momento de enviar el mail.')
    
    messages.success(request, "Venta finalizada con éxito.")  
    
    return redirect('ventas:listar_ventas_cajero')

def ReporteCuentaCorrienteClientes(request):
    
    sucursalesIds = []

    rolesFromQuery = Rol.objects.filter(opciones='GERENTE GENERAL')
    rolId = ""
    for rol in rolesFromQuery:
        print(rol.id)
        rolId = rol.id

    es_gerente_general = request.user.rol_id == rolId
    print("es_gerente_general: " + str(es_gerente_general))
    
    sucursal_asociada = ""
    VentasFromQuery = Venta.objects.all()
    
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

    print("sucursalesIds: %s" % sucursalesIds)
    
    lista = []
    for fila in VentasFromQuery:
        print(fila.sucursal_asociada_id)
        print(sucursalesIds)
        if fila.sucursal_asociada_id in sucursalesIds:
            lista.append(fila)
    print(lista)
    ventas = []

    for venta in lista:
        dic = {
            "numero_comprobante": venta.numero_comprobante,
            "cuenta_corriente_numero_cuenta": venta.cuenta_corriente.numero_cuenta,
            "sucursal_asociada_codigo": venta.sucursal_asociada.codigo,
            "cliente_asociado_nombre": venta.cliente_asociado.nombre,
            "mediodepago": venta.mediodepago,
            "fecha": venta.fecha,
            "tipo_de_moneda": venta.tipo_de_moneda,
            "tipo_de_moneda_opciones": venta.tipo_de_moneda.opciones,
            "total_dolar": venta.total_dolar,
            "total_euro": venta.total_euro,
            "total_peso": venta.total_peso,
            "fecha_a_comparar": str(venta.fecha.date()),
            "es_gerente_general": str(es_gerente_general),
            "sucursales": sucursalesIds,
            "sucursal_asociada_id": venta.sucursal_asociada_id
        }
        ventas.append(dic)

    return render(request,'ventas/reporte_cuenta_corriente_clientes.html',locals())


def verComprobantePago(request, venta_id):
    
    query = ComprobantePago.objects.filter(numero_venta = venta_id)
    lista = []
    
    for info in query:
        
        lista.append(info)
        
    return render(request, 'ventas/ver_comprobante.html', locals())

def ReporteVentasVendedores(request):
    sucursalesIds = []

    rolesFromQuery = Rol.objects.filter(opciones='GERENTE GENERAL')
    rolId = ""
    for rol in rolesFromQuery:
        print(rol.id)
        rolId = rol.id

    es_gerente_general = request.user.rol_id == rolId
    print("es_gerente_general: " + str(es_gerente_general))
    
    sucursal_asociada = ""

    QueryEstados = EstadoVenta.objects.filter(opciones = 'PAGADA')
    estado_pagada = ""
    
    for estado in QueryEstados:
        
        estado_pagada = estado.id
    
    
    ItemFromQuery = Venta.objects.filter(estado = estado_pagada).values('vendedor_asociado_id').annotate(Count('vendedor_asociado_id')).order_by()
    
    
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

    print("sucursalesIds: %s" % sucursalesIds)
    
    ventas = []
    dic_vendedores = {}
    
    for venta in ItemFromQuery:
        
        ventas.append(venta.get('vendedor_asociado_id'))
        dic_vendedores.update({venta.get('vendedor_asociado_id'):venta.get('vendedor_asociado_id__count')})
        
    
    
    vendedor_obtenido = Vendedor.objects.raw("""
     SELECT *
     FROM usuario_vendedor
     WHERE usuario_ptr_id IN %s                                                                                 
     """, [tuple(ventas)])
    
    
    VentaFromQuery = Venta.objects.raw(""" 
     SELECT *
     FROM venta_venta
     WHERE vendedor_asociado_id IN %s                                                                                 
     """, [tuple(ventas)])
    
    total = 0
    dic_ventas = {}
    for venta in VentaFromQuery:
        
        if not dic_ventas.__contains__(venta.vendedor_asociado_id):
            dic_ventas.update({venta.vendedor_asociado_id: 0})
        
        dic_ventas.update({venta.vendedor_asociado_id:dic_ventas.get(venta.vendedor_asociado_id)+venta.monto_ingresado})
        
    
    lista = []
    for fila in vendedor_obtenido:
        print(fila.sucursal_id)
        print(sucursalesIds)
        if fila.sucursal_id in sucursalesIds:
            lista.append(fila)
    print(lista)
    
    items = []

    for vendedor in lista:
        dic = {
            "vendedor": vendedor.nombre,
            "cantidad_ventas": dic_vendedores.get(vendedor.id),
            "sucursal_id": vendedor.sucursal_id,
            "total": dic_ventas.get(vendedor.id),
        }
        items.append(dic)

    
    return render(request, 'ventas/reporte_ventas_vendedor.html', locals())

def reporteVentasPorSucursal(request):
    sucursalesIds = []

    rolesFromQuery = Rol.objects.filter(opciones='GERENTE GENERAL')
    rolId = ""
    for rol in rolesFromQuery:
        print(rol.id)
        rolId = rol.id

    es_gerente_general = request.user.rol_id == rolId
    print("es_gerente_general: " + str(es_gerente_general))

    sucursal_asociada = ""

    QueryEstados = EstadoVenta.objects.filter(opciones = 'PAGADA')
    estado_pagada = ""

    for estado in QueryEstados:

        estado_pagada = estado.id


    ItemFromQuery = Venta.objects.filter(estado = estado_pagada).values('sucursal_asociada_id').annotate(Count('sucursal_asociada_id')).order_by()


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

    print("sucursalesIds: %s" % sucursalesIds)

    ventas = []
    dic_sucursales = {}

    for venta in ItemFromQuery:
        dic_sucursales.update({venta.get('sucursal_asociada_id'):venta.get('sucursal_asociada_id_count')})
        ventas.append(venta.get('sucursal_asociada_id'))


    VentaFromQuery = Venta.objects.raw(""" 
     SELECT *
     FROM venta_venta
     WHERE sucursal_asociada_id IN %s
     """, [tuple(ventas)])

    total = 0
    dic_ventas = {}
    for venta in VentaFromQuery:

        if not dic_ventas.__contains__(venta.sucursal_asociada_id):
            dic_ventas.update({venta.sucursal_asociada_id: 0})

        dic_ventas.update({venta.sucursal_asociada_id:dic_ventas.get(venta.sucursal_asociada_id)+venta.monto_ingresado})


    lista = []
    for fila in VentaFromQuery:
        print(fila.sucursal_asociada_id)
        print(sucursalesIds)
        if fila.sucursal_asociada_id in sucursalesIds:
            lista.append(fila)
    print(lista)

    items = []

    for venta in lista:
        dic = {
            "cantidad_ventas": dic_sucursales.get(venta.sucursal_asociada_id),
            "sucursal_id": venta.sucursal_asociada_id,
            "total": dic_ventas.get(venta.sucursal_asociada_id),
            "sucursal_asociada_codigo": venta.sucursal_asociada.codigo,
        }
        items.append(dic)


    return render(request, 'ventas/reporte_ventas_por_sucursal.html', locals())