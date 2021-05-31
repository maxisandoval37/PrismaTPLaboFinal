from django.contrib.admin import ModelAdmin, register
from .models import Venta, EstadoVenta, VentaLocal, ItemVenta
# Register your models here.


@register(Venta)
class ventaADMIN(ModelAdmin):
    icon_name = 'person'
    
@register(EstadoVenta)
class estadoventavirtualADMIN(ModelAdmin):
    icon_name = 'person'
    

@register(VentaLocal)
class ventalocalADMIN(ModelAdmin):
    icon_name = 'person'
    
@register(ItemVenta)
class itemventaADMIN(ModelAdmin):
    
    icon_name = 'person'
    

