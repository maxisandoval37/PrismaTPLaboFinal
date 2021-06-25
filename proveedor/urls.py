from django.urls import path
from django.contrib.auth.decorators import login_required
from proveedor.views import ListadoProveedor, RegistrarProveedor, EditarProveedor, CambiarEstadoCuentaCorriente,CambiarEstadoProveedor, RegistrarCuentaCorrienteProveedor, ListadoCuentasCorriente, EliminarCuentaCorrienteProveedor, verRegistro

urlpatterns = [
    
    path('listado_proveedores/', login_required(ListadoProveedor.as_view()),name='listar_proveedores'),
    path('registrar_proveedor/', login_required(RegistrarProveedor.as_view()),name = 'registrar_proveedor'),
    path('actualizar_proveedor/<int:pk>/', login_required(EditarProveedor.as_view()), name = 'actualizar_proveedor'),
    path('cambiar_estado/<int:pk>/',login_required(CambiarEstadoProveedor.as_view()), name='cambiar_estado'),
    path('registrar_cuenta_corriente/', login_required(RegistrarCuentaCorrienteProveedor.as_view()), name='registrar_cuenta_corriente'),
    path('listado_cuenta_corriente/', login_required(ListadoCuentasCorriente.as_view()), name='listar_cuenta_corriente'),
    path('eliminar_cuenta_corriente/<int:pk>/', login_required(EliminarCuentaCorrienteProveedor.as_view()), name= 'eliminar_cuenta_corriente'),
    path('ver_registro/<int:cuentacorriente>/', login_required(verRegistro), name= 'ver_registro'),
    path('cambiar_estado_cuenta/<int:pk>/', login_required(CambiarEstadoCuentaCorriente.as_view()), name = 'cambiar_estado_cuenta'),
]