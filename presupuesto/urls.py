from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from .views import ListadoPresupuesto, RegistrarPresupuesto, EliminarPresupuesto

urlpatterns = [
    
    path('listado_presupuestos/', login_required(ListadoPresupuesto.as_view()),name='listar_presupuestos'),
    path('registrar_presupuesto/', login_required(RegistrarPresupuesto.as_view()),name = 'registrar_presupuesto'),
    path('eliminar_presupuesto/<int:pk>/',login_required(EliminarPresupuesto.as_view()), name='eliminar_presupuesto'),
    
]