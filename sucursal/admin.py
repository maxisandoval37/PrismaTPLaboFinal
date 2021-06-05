from django.contrib.admin import ModelAdmin, register
from .models import Sucursal, Caja, Operacion

@register(Sucursal)
class sucursalAdmin(ModelAdmin):
    
    icon_name = 'home'



@register(Caja)
class cajaADmin(ModelAdmin):
    
    icon_name = 'home'
    
    
@register(Operacion)
class operacionAdmin(ModelAdmin):
    
    icon_name = 'home'