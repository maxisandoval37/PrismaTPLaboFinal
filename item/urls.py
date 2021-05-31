from django.urls import path
from .views import ListaItemsPorCriterio, RegistrarItem,EditarItem,EliminarItem, ConfigurarReposicionItem, ListarCategorias,ListarPedidos,  VerPedido,RecibirStock, MensajeExitoso
from django.contrib.auth.decorators import login_required

urlpatterns = [
    
    path('listado_items/', login_required(ListaItemsPorCriterio) ,name='listar_items'),
    path('registrar_item/', login_required(RegistrarItem.as_view()),name = 'registrar_item'),
    path('actualizar_item/<int:pk>/', login_required(EditarItem.as_view()), name = 'actualizar_item'),
    path('eliminar_item/<int:pk>/',login_required(EliminarItem.as_view()), name='eliminar_item'),
    path('reposicion_item/<int:pk>/', login_required(ConfigurarReposicionItem.as_view()), name='reposicion_item'),
    path('listar_categorias/', login_required(ListarCategorias.as_view()), name = 'listar_categorias'),
    path('visualizar_pedidos/', login_required(ListarPedidos.as_view()) ,name='visualizar_pedidos'),
    path('pedido_proveedor/<int:id_proveedor>/<int:id_sucursal>/', VerPedido, name= 'pedido_proveedor'),
    path('pedido_proveedor/<int:id_proveedor>/<int:id_sucursal>/RecibirStock/', RecibirStock, name= 'pedido_proveedor'),
    path('stock_recibido/', MensajeExitoso.as_view(), name= 'stock_recibido'),
    
    
]