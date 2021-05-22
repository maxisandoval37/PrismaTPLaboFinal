from django.contrib.admin import ModelAdmin, register
from django.db import models
from .models import Cliente, EstadoCliente, EstadoDeuda, Deuda, CategoriaCliente, MedioDePago, CuentaCorriente

@register(Cliente)
class clienteADMIN(ModelAdmin):
    
    icon_name = 'person'
    
@register(EstadoCliente)
class estadoclienteADMIN(ModelAdmin):
    
    icon_name = 'person'

@register(Deuda)
class deudaADMIN(ModelAdmin):
    icon_name = 'person'
@register(EstadoDeuda)
class estadodeudaADMIN(ModelAdmin):
    icon_name = 'person'
@register(CategoriaCliente)
class catADMIN(ModelAdmin):
    icon_name = 'person'

@register(MedioDePago)
class mdpADMIN(ModelAdmin):
    icon_name = 'person'
    
@register(CuentaCorriente)
class ccADMIN(ModelAdmin):
    icon_name = 'person'