from django import forms
from .models import VentaLocal, VentaVirtual


class VentaLocalForm(forms.ModelForm):
    
    class Meta:
        model = VentaLocal
        fields = '__all__'
        
class VentaVirtualForm(forms.ModelForm):
    
    class Meta:
        model = VentaVirtual
        fields = '__all__'
        
        