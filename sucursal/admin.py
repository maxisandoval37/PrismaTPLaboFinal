from django.contrib.admin import ModelAdmin, register
from .models import Sucursal

@register(Sucursal)
class sucursalAdmin(ModelAdmin):
    
    icon_name = 'home'



