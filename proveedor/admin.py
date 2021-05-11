from django.contrib.admin import ModelAdmin, register
from .models import Proveedor


@register(Proveedor)
class provAdmin(ModelAdmin):
    
    icon_name = 'person_add'
