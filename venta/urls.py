from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from .views import ListadoVenta, RegistrarVentaLocal, RegistrarVentaVirtual, EliminarVenta, ListarItem, AgregarItemVenta

urlpatterns = [
    
    path('listado_ventas/', login_required(ListadoVenta.as_view()),name='listar_ventas'),
    path('registrar_venta_local/', login_required(RegistrarVentaLocal.as_view()),name = 'registrar_venta_local'),
    path('registrar_venta_virtual/', login_required(RegistrarVentaVirtual.as_view()),name = 'registrar_venta_virtual'),
    path('eliminar_venta/<int:pk>/',login_required(EliminarVenta.as_view()), name='eliminar_venta'),
    path('listado_itemsventa/<int:venta>/', login_required(ListarItem), name= 'listar_itemsventa'),
    path('registrar_itemventa/<int:pk>/<int:sucursal_asociada>/', login_required(AgregarItemVenta.as_view()), name= 'registrar_itemventa'),
    
   
]