from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import ListadoCliente, RegistrarCliente, EditarCliente, RegistrarMDP, RegistrarCuentaCorriente

urlpatterns = [
    
    path('listado_clientes/', login_required(ListadoCliente.as_view()),name='listar_clientes'),
    path('registrar_cliente/', login_required(RegistrarCliente.as_view()),name = 'registrar_cliente'),
    path('actualizar_cliente/<int:pk>/', login_required(EditarCliente.as_view()), name = 'actualizar_cliente'),
    path('registrar_cuenta_corriente/', login_required(RegistrarCuentaCorriente.as_view()), name='registrar_cuenta_corriente'),
    path('registrar_mdp/', login_required(RegistrarMDP.as_view()),name = 'registrar_mdp'),
]