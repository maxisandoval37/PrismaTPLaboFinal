from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import ListadoPresupuesto, RegistrarPresupuesto, ListarItem, VerDetalle, AgregarItem, AprobarPresupuesto, RechazarPresupuesto, eliminarItem

urlpatterns = [
    
    path('listado_presupuestos/', login_required(ListadoPresupuesto.as_view()),name='listar_presupuestos'),
    path('registrar_presupuesto/', login_required(RegistrarPresupuesto.as_view()),name = 'registrar_presupuesto'),
    path('listado_itemspresupuesto/<int:presupuesto>/', login_required(ListarItem), name= 'listar_itemspresupuesto'),
    path('registrar_itempresupuesto/<int:sucursal>/<int:presupuesto>', login_required(VerDetalle), name= 'registrar_itempresupuesto'),
    path('registrar_itempresupuesto/<int:sucursal>/<int:presupuesto>/AgregarItem/', login_required(AgregarItem), name= 'agregar_item'),
    path('aprobar_presupuesto/<int:id>/', login_required(AprobarPresupuesto), name= 'aprobar_presupuesto'),
    path('rechazar_presupuesto/<int:id>/', login_required(RechazarPresupuesto), name= 'rechazar_presupuesto'),
    path('eliminar_item/<int:presupuesto>/<int:item>/', login_required(eliminarItem), name = 'eliminar_item'),
]