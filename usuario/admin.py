from django.contrib.admin import ModelAdmin, register
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from usuario.models import Rol, Usuario, Estado

@register(Rol)
class MaterialRolAdmin(ModelAdmin):
    icon_name = 'person'

@register(Permission)
class MaterialPermAdmin(ModelAdmin):
    icon_name = 'lock'

@register(Usuario)
class usuarioAdmin(ModelAdmin):
    
    icon_name = 'person'
    
    
@register(Estado)
class estadoAdmin(ModelAdmin):
    
    icon_name = 'access_time'    