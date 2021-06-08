from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import ListadoCliente, RegistrarCliente, EditarCliente, RegistrarMDP, RegistrarCuentaCorriente, ListadoCuentasCorriente, EliminarCuentaCorriente, verRegistro, consultaDiaria, consultaHistorico

urlpatterns = [
    
    path('listado_clientes/', login_required(ListadoCliente.as_view()),name='listar_clientes'),
    path('registrar_cliente/', login_required(RegistrarCliente.as_view()),name = 'registrar_cliente'),
    path('actualizar_cliente/<int:pk>/', login_required(EditarCliente.as_view()), name = 'actualizar_cliente'),
    path('registrar_cuenta_corriente/', login_required(RegistrarCuentaCorriente.as_view()), name='registrar_cuenta_corriente'),
    path('registrar_mdp/', login_required(RegistrarMDP.as_view()),name = 'registrar_mdp'),
    path('listado_cuenta_corriente/', login_required(ListadoCuentasCorriente.as_view()), name='listar_cuenta_corriente'),
    path('eliminar_cuenta_corriente/<int:pk>/', login_required(EliminarCuentaCorriente.as_view()), name='eliminar_cuenta_corriente'),
    path('ver_registro/<int:cuentacorriente>/', login_required(verRegistro), name= 'ver_registro'),
    path('consulta_cotizaciones/', login_required(consultaDiaria),name='consulta_cotizaciones'),
    path('consultas_historico/', login_required(consultaHistorico), name='consultas_historico'),
]