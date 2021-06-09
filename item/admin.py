from django.contrib.admin import ModelAdmin, register
from .models import Item, Estado, Categoria, UnidadDeMedida, SubCategoria, Pedidos, Pintura, Mezcla, PinturaUsada, PinturaNueva, ReportePrecios

@register(Item)
class itemAdmin(ModelAdmin):
    
    icon_name = 'add_box' 
    
@register(Estado)
class estadoAdmin(ModelAdmin):
    
    icon_name = 'hourglass_empty'

@register(Categoria)
class categoriaAdmin(ModelAdmin):
    
    icon_name = 'grade'
    
@register(UnidadDeMedida)
class unidadMedidaAdmin(ModelAdmin):
    
    icon_name = 'loop'
    
@register(SubCategoria)
class subcatAdmin(ModelAdmin):
    
    icon_name = 'grade'
    
@register(Pedidos)
class pedidosAdmin(ModelAdmin):
    
    icon_name = 'add_box'
    
@register(Pintura)
class pinturaAdmin(ModelAdmin):
    
    icon_name = 'add_box'
    
@register(PinturaNueva)
class pinturanuevaAdmin(ModelAdmin):
    
    icon_name = 'add_box'

@register(PinturaUsada)
class pinturaSAdmin(ModelAdmin):
    
    icon_name = 'add_box'
    
@register(Mezcla)
class mezclaAdmin(ModelAdmin):
    
    icon_name = 'add_box'
    
@register(ReportePrecios)
class auditoriapreciosADMIN(ModelAdmin):
    
    icon_name = 'add_box'

    
