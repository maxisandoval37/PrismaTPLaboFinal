from django.contrib.admin import ModelAdmin, register
from .models import Proveedor, CuentaCorrienteProveedor, EstadoProveedor, EstadoCuentaCorriente



@register(Proveedor)
class provAdmin(ModelAdmin):
    
    icon_name = 'person_add'

@register(CuentaCorrienteProveedor)
class ccAdmin(ModelAdmin):
    
    icon_name = 'person_add'
    
@register(EstadoProveedor)
class estAdmin(ModelAdmin):
    
    icon_name = 'person_add'
    
@register(EstadoCuentaCorriente)
class estctAdmin(ModelAdmin):
    
    icon_name = 'person_add'