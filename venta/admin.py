from django.contrib.admin import ModelAdmin, register
from .models import Venta, EstadoVenta, VentaLocal, ItemVenta, Cotizacion, ComprobantePago



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
    
@register(Cotizacion)
class cotadmin(ModelAdmin):
    
    icon_name = 'person'
    
@register(ComprobantePago)
class comprobantepagoADMIN(ModelAdmin):
    
    icon_name = 'person'
