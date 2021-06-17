from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from .views import ListadoVenta, RegistrarVentaLocal, EditarVentaLocal, eliminarItemCajero, EliminarVenta, ListarItem, VerDetalle, AgregarItem, CambiarEstado, eliminarItem, ListadoVentaCajero, FinalizarVenta, VerItems, ReporteCuentaCorrienteClientes, verComprobantePago

urlpatterns = [

    path('listado_ventas/', login_required(ListadoVenta.as_view()),
         name='listar_ventas'),
    path('registrar_venta_local/', login_required(RegistrarVentaLocal.as_view()),
         name='registrar_venta_local'),
    path('ingresar_monto/<int:pk>/',
         login_required(EditarVentaLocal.as_view()), name='ingresar_monto'),
    path('eliminar_venta/<int:pk>/',
         login_required(EliminarVenta.as_view()), name='eliminar_venta'),
    path('listado_itemsventa/<int:venta>/',
         login_required(ListarItem), name='listar_itemsventa'),
    path('registrar_itemventa/<int:sucursal>/<int:venta>',
         login_required(VerDetalle), name='registrar_itemventa'),
    path('registrar_itemventa/<int:sucursal>/<int:venta>/AgregarItem/',
         login_required(AgregarItem), name='agregar_item'),
    path('listado_ventas/<int:id>/<int:cliente>/',
         login_required(CambiarEstado), name='cambiar_estado'),
    path('eliminar_item/<int:venta>/<int:item>/',
         login_required(eliminarItem), name='eliminar_item'),
    path('eliminar_item_cajero/<int:venta>/<int:item>/',
         login_required(eliminarItemCajero), name='eliminar_item_cajero'),
    path('listado_ventas_cajero/', login_required(ListadoVentaCajero.as_view()),
         name='listar_ventas_cajero'),
    path('finalizar_venta/<int:venta>/',
         login_required(FinalizarVenta), name='finalizar_venta'),
    path('ver_items/<int:venta>/', login_required(VerItems), name='ver_items'),
    path('reporte_cuenta_corriente_clientes/', login_required(
        ReporteCuentaCorrienteClientes), name='reporte_cuenta_corriente_clientes'),
    path('ver_comprobante/<int:venta_id>/', login_required(verComprobantePago), name= 'ver_comprobante'),
        
]
