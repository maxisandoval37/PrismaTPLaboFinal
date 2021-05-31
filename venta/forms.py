from django import forms
from .models import VentaLocal, VentaVirtual, ItemVenta
from django.core.exceptions import ValidationError

class VentaLocalForm(forms.ModelForm):
    
    class Meta:
        model = VentaLocal
        fields = ['numero_comprobante','estado','cliente_asociado','mediodepago','sucursal_asociada','vendedor_asociado','cuenta_corriente']
    
           
           
class VentaVirtualForm(forms.ModelForm):
    
    class Meta:
        model = VentaVirtual
        fields = '__all__'
        
    
class ItemVentaForm(forms.ModelForm):
    
    class Meta:
        model = ItemVenta
        fields = ['item','cantidad_solicitada','monto','sucursal_asociada','venta_asociada']
                