from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormView
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, ListView, FormView
from .models import Usuario
from django.contrib.auth.mixins import PermissionRequiredMixin
from .forms import FormularioLogin, FormularioUsuario
from .mixins import ValidarLoginYPermisosRequeridos



class Login(FormView):
    template_name = 'login.html'
    form_class = FormularioLogin
    success_url = reverse_lazy('index')

    # medidas adicionales de seguridad ;)

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(Login,self).dispatch(request, *args, **kwargs)
        
    def form_valid(self, form):
        login(self.request,form.get_user())
        return super(Login,self).form_valid(form)

def logoutUsuario(request):
    logout(request)
    return HttpResponseRedirect('/accounts/login/')


class Inicio(TemplateView):
    template_name = 'index.html'
    
class InicioUsuarios(ValidarLoginYPermisosRequeridos, TemplateView):
    permission_required = ('usuario.view_usuario','usuario.add_usuario','usuario.delete_usuario','usuario.change_usuario',)
    template_name = 'usuarios/listar_usuario.html'

    
class ListadoUsuario(ValidarLoginYPermisosRequeridos,ListView):
     model = Usuario
     template_name = 'usuarios/listar_usuario.html'
     queryset = Usuario.objects.filter(is_staff = False)
     
    
class RegistrarUsuario(ValidarLoginYPermisosRequeridos,CreateView):
    model = Usuario
    form_class = FormularioUsuario
    template_name = 'usuarios/crear_usuario.html'
    success_url = reverse_lazy('usuarios:listar_usuarios')
    
   


class EditarUsuario(ValidarLoginYPermisosRequeridos,UpdateView):
    
    model = Usuario
    fields = ['nombre','apellido','email','telefono','rol']
    template_name = 'usuarios/editar_usuario.html'
    success_url = reverse_lazy('usuarios:listar_usuarios')
    
    
    





    