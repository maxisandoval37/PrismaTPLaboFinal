from django.contrib import admin
from django.conf import settings
from django.views.static import serve
from django.urls import path,include,re_path
from django.contrib.auth.decorators import login_required
from usuario.views import Inicio,Login,logoutUsuario
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('usuarios/',include(('usuario.urls','usuarios'))),
    path('items/', include(('item.urls','items'))),
    path('sucursales/', include(('sucursal.urls','sucursales'))),
    path('proveedores/', include(('proveedor.urls','proveedores'))),
    path('',login_required(Inicio.as_view()), name = 'index'),
    path('accounts/login/',Login.as_view(), name = 'login'),
    path('logout/',login_required(logoutUsuario),name = 'logout'),
    path('reset_password/', auth_views.PasswordResetView.as_view(), name = 'reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name = 'password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name = 'password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name = 'password_reset_complete'),
]