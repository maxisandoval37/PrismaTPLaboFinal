from django.urls import path
from .views import ListarSucursal, RegistrarCaja,RegistrarSucursal,EditarSucursal, idSucursal, idCaja, consolidacionSucursales, consolidacionPorSucursal, ReporteTransaccionesVentaCompra, ExtraerDinero
from django.contrib.auth.decorators import login_required

urlpatterns = [
    
    path('listado_sucursales/', login_required(ListarSucursal) ,name='listar_sucursales'),
    path('registrar_sucursal/', login_required(RegistrarSucursal.as_view()),name = 'registrar_sucursal'),
    path('editar_sucursal/<int:pk>/',login_required(EditarSucursal.as_view()), name='editar_sucursal'),
    path('visualizar_items/<int:id>/', login_required(idSucursal), name= 'visualizar_items'),
    path('visualizar_cajas/<int:id>/', login_required(idCaja), name= 'visualizar_cajas'),
    path('visualizar_cajas/<int:id>/ExtraerDinero/', login_required(ExtraerDinero), name= 'extraer_dinero'),
    path('consolidado_sucursales/', login_required(consolidacionSucursales), name = 'consolidado_sucursales'),
    path('consolidado_sucursal/<int:id>', login_required(consolidacionPorSucursal), name = 'consolidado_sucursal'),
    path('registrar_caja/', login_required(RegistrarCaja.as_view()), name = 'registrar_caja'),
    path('reporte_transacciones_venta_compra/', login_required(ReporteTransaccionesVentaCompra), name='reporte_transacciones_venta_compra'),
    
    
]