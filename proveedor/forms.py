from django import forms
from .models import Proveedor, CuentaCorrienteProveedor


class ProveedorForm(forms.ModelForm):
    

    class Meta:
        model = Proveedor
        fields = '__all__'
       
       
class CuentaCorrienteProveedorForm(forms.ModelForm):
    
    class Meta:
        model = CuentaCorrienteProveedor
        fields = '__all__'