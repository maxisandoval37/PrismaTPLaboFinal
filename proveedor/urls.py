from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from proveedor.views import ListadoProveedor, RegistrarProveedor, EditarProveedor, EliminarProveedor, RegistrarCuentaCorrienteProveedor, ListadoCuentasCorriente, EliminarCuentaCorrienteProveedor, verRegistro

urlpatterns = [
    
    path('listado_proveedores/', login_required(ListadoProveedor.as_view()),name='listar_proveedores'),
    path('registrar_proveedor/', login_required(RegistrarProveedor.as_view()),name = 'registrar_proveedor'),
    path('actualizar_proveedor/<int:pk>/', login_required(EditarProveedor.as_view()), name = 'actualizar_proveedor'),
    path('eliminar_proveedor/<int:pk>/',login_required(EliminarProveedor.as_view()), name='eliminar_proveedor'),
    path('registrar_cuenta_corriente/', login_required(RegistrarCuentaCorrienteProveedor.as_view()), name='registrar_cuenta_corriente'),
    path('listado_cuenta_corriente/', login_required(ListadoCuentasCorriente.as_view()), name='listar_cuenta_corriente'),
    path('eliminar_cuenta_corriente/<int:pk>/', login_required(EliminarCuentaCorrienteProveedor.as_view()), name= 'eliminar_cuenta_corriente'),
    path('ver_registro/<int:cuentacorriente>/', login_required(verRegistro), name= 'ver_registro'),
]