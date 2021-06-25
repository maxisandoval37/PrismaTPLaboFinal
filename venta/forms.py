from django import forms
from .models import VentaLocal, ItemVenta

class VentaLocalForm(forms.ModelForm):
    
    
    class Meta:
        model = VentaLocal
        fields = ['cliente_asociado','mediodepago','tipo_de_moneda','sucursal_asociada','vendedor_asociado','cuenta_corriente']
    
           
           
    
class ItemVentaForm(forms.ModelForm):
    
    class Meta:
        model = ItemVenta
        fields = ['item','cantidad_solicitada','monto','sucursal_asociada','venta_asociada']
                