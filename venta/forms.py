from django import forms
from .models import VentaLocal, VentaVirtual
from django.core.exceptions import ValidationError
from sucursal.models import Caja

class VentaLocalForm(forms.ModelForm):
    
    class Meta:
        model = VentaLocal
        fields = ['numero_comprobante','cliente_asociado','mediodepago','item_asociado','sucursal_asociada','vendedor_asociado','monto','cantidad_solicitada','cuenta_corriente']
        
           
class VentaVirtualForm(forms.ModelForm):
    
    class Meta:
        model = VentaVirtual
        fields = '__all__'
        
    
                