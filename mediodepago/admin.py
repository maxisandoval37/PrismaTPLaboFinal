from django.contrib.admin import ModelAdmin, register
from .models import  MedioDePago, TipoDePago


@register(MedioDePago)
class mdpAdmin(ModelAdmin):
    
    icon_name = 'monetization_on'
    
@register(TipoDePago)
class tipodepagoAdmin(ModelAdmin):
    icon_name = 'monetization_on'
"""     
@register(Efectivo)
class efectivoAdmin(ModelAdmin):
    
    icon_name = 'monetization_on'
    
@register(Transferencia)
class transferenciaAdmin(ModelAdmin):
    
    icon_name = 'monetization_on'
    
@register(Cheque)
class chequeAdmin(ModelAdmin):
    
    icon_name = 'monetization_on'
    
@register(TipoTarjeta)
class tipotarjetaAdmin(ModelAdmin):

    icon_name = 'monetization_on'
    
@register(Tarjeta)
class tarjetaAdmin(ModelAdmin):
    
    icon_name = 'monetization_on'
    
@register(MercadoPago)
class mercadopagoAdmin(ModelAdmin):
    icon_name = 'monetization_on'
    
 """