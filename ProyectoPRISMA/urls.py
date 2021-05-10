from django.contrib import admin
from django.conf import settings
from django.views.static import serve
from django.urls import path,include,re_path
from django.contrib.auth.decorators import login_required
from usuario.views import Inicio,Login,logoutUsuario

urlpatterns = [
    path('admin/', admin.site.urls),
    path('usuarios/',include(('usuario.urls','usuarios'))),
    path('',login_required(Inicio.as_view()), name = 'index'),
    path('accounts/login/',Login.as_view(), name = 'login'),
    path('logout/',login_required(logoutUsuario),name = 'logout'),
]