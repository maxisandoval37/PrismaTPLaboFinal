from django.contrib.admin import ModelAdmin, register
from .models import Presupuesto, EstadoPresupuesto

@register(Presupuesto)
class presupuestoADMIN(ModelAdmin):
    
    icon_name = 'person'
    
@register(EstadoPresupuesto)
class estadopresupuestoADMIN(ModelAdmin):
    
    icon_name = 'person'


