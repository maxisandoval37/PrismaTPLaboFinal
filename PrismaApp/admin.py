from django.contrib.admin import ModelAdmin, register
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from .models import Usuario, Rol

# Register your models here.



@register(Permission)
class permissionAdmin(ModelAdmin):
    
    pass


@register(Usuario)
class usuarioAdmin(ModelAdmin):
    
    list_display=("username","cuit","email",)
    icon_name = 'person'
    
@register(Rol)
class rolAdmin(ModelAdmin):
    
    list_display=("rol",)
    icon_name = 'contacts'

