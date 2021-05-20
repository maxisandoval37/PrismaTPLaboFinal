from django.contrib.admin import ModelAdmin, register
from .models import Item, Estado, Categoria, UnidadDeMedida, SubCategoria, Pedidos #CuentaCorrienteProveedor

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
    
# @register(CuentaCorrienteProveedor)
# class cuentacorrienteProvADMIN(ModelAdmin):
#     icon_name = 'person'