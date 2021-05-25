from django.urls import path
from .views import ListadoMDP, RegistrarMDP,EditarMDP,EliminarMDP
from django.contrib.auth.decorators import login_required

urlpatterns = [
    
    path('listado_mdps/', login_required(ListadoMDP.as_view()) ,name='listar_mdps'),
    path('registrar_mdp/', login_required(RegistrarMDP.as_view()),name = 'registrar_mdp'),
    path('actualizar_mdp/<int:pk>/', login_required(EditarMDP.as_view()), name = 'actualizar_mdp'),
    path('eliminar_mdp/<int:pk>/',login_required(EliminarMDP.as_view()), name='eliminar_mdp'),
    
]