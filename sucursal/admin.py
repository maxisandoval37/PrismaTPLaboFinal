from django.contrib.admin import ModelAdmin, register
from .models import Sucursal, Caja

@register(Sucursal)
class sucursalAdmin(ModelAdmin):
    
    icon_name = 'home'



@register(Caja)
class cajaADmin(ModelAdmin):
    
    icon_name = 'home'