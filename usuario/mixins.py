from django.shortcuts import redirect, HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib import messages



class LoginYStaffMixin(object):
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_staff:
                return super().dispatch(request, *args, **kwargs)
        return redirect('index')
    
class ValidarPermisosRequeridos(object):
    
    permission_required = ''
    url_redirect = None
    
    def get_perm(self):
        if isinstance(self.permission_required,str):
            perms = (self.permission_required)
        else:
            perms = self.permission_required
        
        return perms
    
    def get_url_redirect(self):
        if self.url_redirect is None:
            return reverse_lazy('login')
        return self.url_redirect
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.has_perms(self.get_perms()):    # pylint: disable=maybe-no-member
            return super().dispatch(request, *args, **kwargs)   # pylint: disable=maybe-no-member
        
        else:
            messages.error(request, 'Acceso restringuido')
            return HttpResponseRedirect('/error404')
        return redirect(self.get_url_redirect())
            