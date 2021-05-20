from django.contrib.admin import ModelAdmin, register
from .models import Venta, EstadoVentaVirtual, VentaVirtual, VentaLocal
# Register your models here.


@register(Venta)
class ventaADMIN(ModelAdmin):
    icon_name = 'person'
    
@register(EstadoVentaVirtual)
class estadoventavirtualADMIN(ModelAdmin):
    icon_name = 'person'
    
@register(VentaVirtual)
class ventavirtualADMIN(ModelAdmin):
    icon_name = 'person'

@register(VentaLocal)
class ventalocalADMIN(ModelAdmin):
    icon_name = 'person'