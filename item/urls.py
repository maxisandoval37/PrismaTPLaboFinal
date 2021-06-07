from django.urls import path
from .views import ListadoItem, EliminarMezcla, RegistrarItem,EditarItem,EliminarItem, ConfigurarReposicionItem, ListarCategorias,ListarPedidos,  VerPedido,RecibirStock, MensajeExitoso, ModificarCampos, CambioMasivo, ListadoPintura, AgregarPintura, ListadoPinturaUsada,IniciarMezcla, mezclarPinturas, ListadoMezclas, ListadoPinturaNueva, ListadoMezclaUsada, IniciarMezclaUsada, mezclarPinturasUsadas, EliminarMezclaUsada
from django.contrib.auth.decorators import login_required

urlpatterns = [
    
    path('listado_items/', login_required(ListadoItem.as_view()) ,name='listar_items'),
    path('registrar_item/', login_required(RegistrarItem.as_view()),name = 'registrar_item'),
    path('actualizar_item/<int:pk>/', login_required(EditarItem.as_view()), name = 'actualizar_item'),
    path('eliminar_item/<int:pk>/',login_required(EliminarItem.as_view()), name='eliminar_item'),
    path('reposicion_item/<int:pk>/', login_required(ConfigurarReposicionItem.as_view()), name='reposicion_item'),
    path('listar_categorias/', login_required(ListarCategorias.as_view()), name = 'listar_categorias'),
    path('visualizar_pedidos/', login_required(ListarPedidos.as_view()) ,name='visualizar_pedidos'),
    path('pedido_proveedor/<int:id_proveedor>/<int:id_sucursal>/', VerPedido, name= 'pedido_proveedor'),
    path('pedido_proveedor/<int:id_proveedor>/<int:id_sucursal>/RecibirStock/', RecibirStock, name= 'pedido_proveedor'),
    path('stock_recibido/', MensajeExitoso.as_view(), name= 'stock_recibido'),
    path('ver_categorias/', ModificarCampos.as_view(), name= 'ver_categorias'),
    path('ver_categorias/CambioMasivo/', CambioMasivo, name='cambio_masivo' ),
    path('listar_pinturas/', login_required(ListadoPintura.as_view()), name='listar_pinturas'),
    path('registrar_pintura/', login_required(AgregarPintura.as_view()), name='registrar_pintura'),
    path('listar_pinturas_nuevas/', login_required(ListadoPinturaNueva.as_view()), name='listar_pinturas_nuevas'),
    path('listar_pinturas_usadas/', login_required(ListadoPinturaUsada.as_view()), name='listar_pinturas_usadas'),
    path('iniciar_mezcla/', login_required(IniciarMezcla.as_view()), name='iniciar_mezcla'),
    path('finalizar_mezcla/<int:mezcla>/<int:primerapintura>/<int:segundapintura>/<int:cantidad_primera>/<int:cantidad_segunda>/', login_required(mezclarPinturas), name='finalizar_mezcla'),
    path('listar_mezclas/', login_required(ListadoMezclas.as_view()), name='listar_mezclas'),
    path('eliminar_mezcla/<int:pk>/', login_required(EliminarMezcla.as_view()), name='eliminar_mezcla'),
    path('iniciar_mezcla_usada/', login_required(IniciarMezclaUsada.as_view()), name='iniciar_mezcla_usada'),
    path('finalizar_mezcla_usada/<int:mezcla>/<int:primerapintura>/<int:segundapintura>/<int:cantidad_primera>/<int:cantidad_segunda>/', login_required(mezclarPinturasUsadas), name='finalizar_mezcla_usada'),
    path('listar_mezclas_usadas/', login_required(ListadoMezclaUsada.as_view()), name='listar_mezclas_usadas'),
    path('eliminar_mezcla_usada/<int:pk>/', login_required(EliminarMezclaUsada.as_view()), name='eliminar_mezcla_usada'),
]