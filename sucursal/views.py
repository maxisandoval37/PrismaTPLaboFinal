from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views.generic import CreateView,DeleteView,ListView,UpdateView, DetailView
from django.urls import reverse_lazy
from .forms import SucursalForm, CajaForm
from .models import Sucursal, Caja, Operacion
from usuario.mixins import ValidarLoginYPermisosRequeridos
from item.models import Item
from django.contrib import messages
from django.db.models import ProtectedError
from django.contrib.messages.views import SuccessMessageMixin
from usuario.models import Rol, Supervisor
from django.http import HttpResponse, HttpResponseBadRequest

def ListarSucursal(request):
    
    lista = []
    
    if request.user.is_staff:
        query = Sucursal.objects.all().order_by('id')

        for info in query:
            lista.append(info)
            
        return render(request, 'sucursales/listar_sucursal.html', locals())
    
    if request.user.rol.opciones == 'SUPERVISOR':
        
        supervisor = ""
        QuerySupervisor = Supervisor.objects.filter(id = request.user.id)
        for info in QuerySupervisor:
            supervisor = info
        
        cod = supervisor.sucursal_id
        sucursal = Sucursal.objects.filter(id = cod)
        
        for suc in sucursal:
            
            lista.append(suc)
    else:
        
        query = Sucursal.objects.all().order_by('id')

        for info in query:
            lista.append(info)
            
    return render(request, 'sucursales/listar_sucursal.html', locals())
        

class RegistrarSucursal(ValidarLoginYPermisosRequeridos,SuccessMessageMixin,CreateView):
    
    permission_required = ('sucursal.view_sucursal','sucursal.add_sucursal',)
    model = Sucursal
    form_class = SucursalForm
    template_name = 'sucursales/crear_sucursal.html'
    success_url = reverse_lazy('sucursales:listar_sucursales')
    success_message = 'Sucursal registrada correctamente.'
    
class EditarSucursal(ValidarLoginYPermisosRequeridos,SuccessMessageMixin,UpdateView):
    
    permission_required = ('sucursal.view_sucursal','sucursal.add_sucursal',)
    model = Sucursal
    fields = ['estado']
    template_name = 'sucursales/editar_sucursal.html'
    success_url = reverse_lazy('sucursales:listar_sucursales')
    success_message = 'El estado de la sucursal se modificó correctamente.'

    
    
class RegistrarCaja(ValidarLoginYPermisosRequeridos,SuccessMessageMixin,CreateView):
    
    permission_required = ('sucursal.view_caja','sucursal.add_caja',)
    model = Caja
    form_class = CajaForm
    template_name = 'sucursales/crear_caja.html'
    success_url = reverse_lazy('sucursales:listar_sucursales')
    success_message = 'Caja registrada correctamente.'
    


def idCaja(request, id):
    
    
    sucursal = Sucursal.objects.get(id = id)
    queryset = Caja.objects.filter(sucursal_id = sucursal.id)
    lista = []
    for caja in queryset:
        dic = {
            "caja_id": caja.id,
            "caja_codigo": caja.codigo,
            "saldo_disponible": caja.saldo_disponible,
            "saldo_disponible_dolares": caja.saldo_disponible_dolares,
            "saldo_disponible_euros": caja.saldo_disponible_euros,
            "ingresos_en_pesos": caja.ingresos_en_pesos,
            "ingresos_en_dolares": caja.ingresos_en_dolares,
            "ingresos_en_euros": caja.ingresos_en_euros,
            "egresos": caja.egresos,
            "saldo_inicial": caja.saldo_inicial,
            "saldo_final": caja.saldo_final,
            "sucursal_id": caja.sucursal_id,
            
        }
        lista.append(dic) 
   
    
    return render(request, 'sucursales/visualizar_cajas.html',locals())
    

    
    
def idSucursal(request, id):
    
    sucursal = Sucursal.objects.get(id = id)
    queryset = Item.objects.filter(sucursal = sucursal.id)
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
        }
        lista.append(dic) 
   
    
    return render(request, 'sucursales/visualizar_items.html',locals())
    

def consolidacionSucursales(request):
    
    cajas = Caja.objects.all()
    lista = []
    egresosTotal = 0
    ingresos_en_pesos = 0
    ingresos_en_dolares = 0
    ingresos_en_euros = 0
    lista = []
    for caja in cajas:
        
        egresosTotal += caja.egresos
        ingresos_en_pesos += caja.ingresos_en_pesos
        ingresos_en_dolares += caja.ingresos_en_dolares 
        ingresos_en_euros += caja.ingresos_en_euros
        
        
    dic = {
        "egresos": egresosTotal,
        "ingresos_en_pesos": ingresos_en_pesos,
        "ingresos_en_dolares": ingresos_en_dolares,
        "ingresos_en_euros": ingresos_en_euros,
    }
    lista.append(dic)
    
    return render(request, 'sucursales/consolidado.html', locals())

def consolidacionPorSucursal(request, id):
    
    sucursal = Sucursal.objects.get(id = id)
    cajas = Caja.objects.filter(sucursal_id = sucursal.id)
    egresosTotal = 0
    ingresos_en_pesos = 0
    ingresos_en_dolares = 0
    ingresos_en_euros = 0
    lista = []
    for caja in cajas:
        
        egresosTotal += caja.egresos
        ingresos_en_pesos += caja.ingresos_en_pesos
        ingresos_en_dolares += caja.ingresos_en_dolares 
        ingresos_en_euros += caja.ingresos_en_euros
        
        
    dic = {
        "egresos": egresosTotal,
        "ingresos_en_pesos": ingresos_en_pesos,
        "ingresos_en_dolares": ingresos_en_dolares,
        "ingresos_en_euros": ingresos_en_euros,
    }
    lista.append(dic)
    
    return render(request, 'sucursales/consolidadoSucursal.html', locals())

def ReporteTransaccionesVentaCompra(request):
    
    sucursalesIds = []

    rolesFromQuery = Rol.objects.filter(opciones='GERENTE GENERAL')
    rolId = ""
    for rol in rolesFromQuery:
        print(rol.id)
        rolId = rol.id

    es_gerente_general = request.user.rol_id == rolId
    print("es_gerente_general: " + str(es_gerente_general))
    
    sucursal_asociada = ""
    OperacionFromQuery = Operacion.objects.all()
    
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
    for fila in OperacionFromQuery:
        
        print(sucursalesIds)
        if fila.caja_asociada.sucursal_id_id in sucursalesIds:
            lista.append(fila)
    print(lista)
    
    operaciones = []

    for operacion in lista:
        dic = {
            "identificador": operacion.identificador,
            "fecha": operacion.fecha,
            "monto": operacion.monto,
            "tipo": operacion.tipo,
            "caja_asociada": operacion.caja_asociada,
            "fecha_a_comparar": str(operacion.fecha.date()),
            "es_gerente_general": str(es_gerente_general),
            "sucursales": sucursalesIds,
            "sucursal_asociada_id": operacion.caja_asociada.sucursal_id_id,
            "responsable": operacion.responsable
            
        }
        operaciones.append(dic)

    return render(request,'sucursales/reporte_transacciones_venta_compra.html',locals())


def ExtraerDinero(request, id):
    
    if request.is_ajax():
        
        cantidad = request.POST.get('cantidad', None)
        caja = request.POST.get('caja', None)
        
        QueryCaja = Caja.objects.filter(codigo = caja)
        print(QueryCaja)
        
        if cantidad.isalpha():
           messages.error(request, "El monto sólo puede contener dígitos.")
           return HttpResponse()
       
        for c in cantidad:
            if c.isalpha():
                messages.error(request, "El monto sólo puede contener dígitos.")
                return HttpResponse() 
            
        if not cantidad.isdigit():
            messages.error(request, "El monto sólo puede contener dígitos.")
            return HttpResponse()
        
        for caja in QueryCaja:
            
            if caja.saldo_disponible < int(cantidad):
                messages.error(request, "La caja no posee suficiente saldo para extraer.")
                return HttpResponse()
            
            elif int(cantidad) < 0:
                messages.error(request, "El monto no puede ser negativo.")
                return HttpResponse()
            
            elif int(cantidad) == 0:
                messages.error(request, 'Debes ingresar un monto a extraer.')
                return HttpResponse()
            
            else:
                
                movimiento = Operacion()
                movimiento.monto = "- " + str(cantidad) + " (En PESO)"
                movimiento.tipo = "Extracción"
                movimiento.caja_asociada_id = caja.id
                movimiento.identificador = "Banco"
                movimiento.responsable = request.user.id
                movimiento.save()
                
                caja.saldo_disponible = caja.saldo_disponible - int(cantidad)
                caja.egresos += int(cantidad)
                caja.save()
        
    messages.success(request, 'Extracción realizada.')
    return HttpResponse("")