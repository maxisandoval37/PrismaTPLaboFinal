from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormView
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, ListView, FormView
from .models import Administrativo, GerenteGeneral, Usuario, Vendedor, Supervisor, Cajero
from .forms import FormularioLogin, FormularioUsuario, FormularioVendedor, FormularioSupervisor, FormularioCajero, FormularioAdministrativo, FormularioGerenteGeneral
from .mixins import ValidarLoginYPermisosRequeridos
from django.contrib.messages.views import SuccessMessageMixin

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
    
class Manual(TemplateView):
    template_name = 'manual.html'
    
class InicioUsuarios(ValidarLoginYPermisosRequeridos, TemplateView):
   
    permission_required = ('usuario.view_usuario',)
    template_name = 'usuarios/listar_usuario.html'
    queryset = Usuario.objects.all().order_by('id')

    
class ListadoUsuario(ValidarLoginYPermisosRequeridos,ListView):
    
     permission_required = ('usuario.view_usuario',)
     model = Usuario
     template_name = 'usuarios/listar_usuario.html'
     queryset = Usuario.objects.filter(is_staff = False)
     
    
class RegistrarUsuario(ValidarLoginYPermisosRequeridos,SuccessMessageMixin,CreateView):
    
    permission_required = ('usuario.view_usuario','usuario.add_usuario',)
    model = Usuario
    form_class = FormularioUsuario
    template_name = 'usuarios/crear_usuario.html'
    success_url = reverse_lazy('usuarios:listar_usuarios')
    success_message = 'Usuario registrado correctamente.'
    


class EditarUsuario(ValidarLoginYPermisosRequeridos,SuccessMessageMixin,UpdateView):
    
    permission_required = ('usuario.view_usuario','usuario.change_usuario',)
    model = Usuario
    fields = ['nombre','apellido','email','telefono']
    template_name = 'usuarios/editar_usuario.html'
    success_url = reverse_lazy('usuarios:listar_usuarios')
    success_message = 'Se editó al usuario correctamente.'
    
class RegistrarVendedor(ValidarLoginYPermisosRequeridos,SuccessMessageMixin,CreateView):
    
    permission_required = ('usuario.view_vendedor','usuario.add_vendedor',)
    model = Vendedor
    form_class = FormularioVendedor
    template_name = 'usuarios/crear_vendedor.html'
    success_url = reverse_lazy('usuarios:listar_usuarios')
    success_message = 'Vendedor registrado correctamente.'
    
class RegistrarSupervisor(ValidarLoginYPermisosRequeridos,SuccessMessageMixin,CreateView):
    
    permission_required = ('usuario.view_supervisor','usuario.add_supervisor',)
    model = Supervisor
    form_class = FormularioSupervisor
    template_name = 'usuarios/crear_supervisor.html'
    success_url = reverse_lazy('usuarios:listar_usuarios')
    success_message = 'Supervisor registrado correctamente.'
    
    
class RegistrarCajero(ValidarLoginYPermisosRequeridos,SuccessMessageMixin,CreateView):
   
    permission_required = ('usuario.view_cajero','usuario.add_cajero',)
    model = Cajero
    form_class = FormularioCajero
    template_name = 'usuarios/crear_cajero.html'
    success_url = reverse_lazy('usuarios:listar_usuarios')
    success_message = 'Cajero registrado correctamente.'

class RegistrarAdministrativo(ValidarLoginYPermisosRequeridos,SuccessMessageMixin,CreateView):
   
    permission_required = ('usuario.view_administrativo','usuario.add_administrativo',)
    model = Administrativo
    form_class = FormularioAdministrativo
    template_name = 'usuarios/crear_administrativo.html'
    success_url = reverse_lazy('usuarios:listar_usuarios')
    success_message = 'Administrativo registrado correctamente.'
    
class RegistrarGerenteGeneral(ValidarLoginYPermisosRequeridos, SuccessMessageMixin, CreateView):
    
    permission_required = ('usuario.view_gerentegeneral','usuario.add_gerentegeneral',)    
    model = GerenteGeneral
    form_class = FormularioGerenteGeneral
    template_name = 'usuarios/crear_gerentegeneral.html'
    success_url = reverse_lazy('usuarios:listar_usuarios')
    success_message = 'Gerente General registrado correctamente.'
    

class CambiarEstadoUsuario(ValidarLoginYPermisosRequeridos, SuccessMessageMixin, UpdateView):
    
    
    permission_required = ('usuario.view_usuario','usuario.add_usuario',)
    model = Usuario
    fields = ['estado']
    template_name = 'usuarios/cambiar_estado.html'
    success_url = reverse_lazy('usuarios:listar_usuarios')
    success_message = 'Se cambió el estado del usuario correctamente.'

    