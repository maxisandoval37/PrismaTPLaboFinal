from django.urls import path
from PrismaApp import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
   
    path('', views.home, name="home"),
    path('registro/', views.registro, name="registro"),
    path('login/',LoginView.as_view(template_name = 'PrismaApp/login.html'), name="login"),
    path('logout/', LogoutView.as_view(template_name = 'PrismaApp/logout.html'), name= 'logout'),
   # path('recuperar/', )
]

urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    