from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from usuario.views import InicioUsuarios,ListadoUsuario, RegistrarUsuario,EditarUsuario
urlpatterns = [
    
    path('inicio_usuarios/', login_required(InicioUsuarios.as_view()), name='inicio_usuarios'),
    path('listado_usuarios/', login_required(ListadoUsuario.as_view()),name='listar_usuarios'),
    path('registrar_usuario/', login_required(RegistrarUsuario.as_view()),name = 'registrar_usuario'),
    path('actualizar_usuario/<int:pk>/', login_required(EditarUsuario.as_view()), name = 'actualizar_usuario'),

    
]

