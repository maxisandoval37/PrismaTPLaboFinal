"""SistemaFerreteria URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from administrarSucursales.class_view import SucursalList,SucursalCreate,SucursalUpdate,SucursalDelete
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',SucursalList.as_view(),name='index'),
    path('crear_sucursal/', SucursalCreate.as_view() ,name='crear_sucursal'),
    path('editar_sucursal/<int:pk>/',SucursalUpdate.as_view(),name='editar_sucursal'),
    path('eliminar_sucursal/<int:pk>/',SucursalDelete.as_view(),name='eliminar_sucursal')

]
