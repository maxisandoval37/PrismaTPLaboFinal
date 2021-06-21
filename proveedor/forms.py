from django import forms
from .models import Proveedor, CuentaCorrienteProveedor


class ProveedorForm(forms.ModelForm):
    

    class Meta:
        model = Proveedor
        fields = ['cuit', 'razon_social','email','telefono','calle','numero','localidad','provincia','cod_postal']
       
       
class CuentaCorrienteProveedorForm(forms.ModelForm):
    
    class Meta:
        model = CuentaCorrienteProveedor
        fields = '__all__'