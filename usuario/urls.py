from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from usuario.views import InicioUsuarios,ListadoUsuario, RegistrarUsuario,EditarUsuario, RegistrarVendedor, RegistrarSupervisor, RegistrarCajero, RegistrarAdministrativo
urlpatterns = [
    
    path('inicio_usuarios/', login_required(InicioUsuarios.as_view()), name='inicio_usuarios'),
    path('listado_usuarios/', login_required(ListadoUsuario.as_view()),name='listar_usuarios'),
    path('registrar_usuario/', login_required(RegistrarUsuario.as_view()),name = 'registrar_usuario'),
    path('actualizar_usuario/<int:pk>/', login_required(EditarUsuario.as_view()), name = 'actualizar_usuario'),
    path('registrar_vendedor/', login_required(RegistrarVendedor.as_view()),name = 'registrar_vendedor'),
    path('registrar_supervisor/', login_required(RegistrarSupervisor.as_view()),name = 'registrar_supervisor'),
    path('registrar_cajero/', login_required(RegistrarCajero.as_view()),name = 'registrar_cajero'),
    path('registrar_administrativo/', login_required(RegistrarAdministrativo.as_view()),name = 'registrar_administrativo'),

    
]

