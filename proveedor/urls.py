from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from proveedor.views import ListadoProveedor, RegistrarProveedor, EditarProveedor, EliminarProveedor

urlpatterns = [
    
    path('listado_proveedores/', login_required(ListadoProveedor.as_view()),name='listar_proveedores'),
    path('registrar_proveedor/', login_required(RegistrarProveedor.as_view()),name = 'registrar_proveedor'),
    path('actualizar_proveedor/<int:pk>/', login_required(EditarProveedor.as_view()), name = 'actualizar_proveedor'),
    path('eliminar_proveedor/<int:pk>/',login_required(EliminarProveedor.as_view()), name='eliminar_proveedor'),
    
]