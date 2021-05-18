from django import forms
from .models import Sucursal, Caja

class SucursalForm(forms.ModelForm):
    
    
    class Meta:
        model = Sucursal
        fields = ['codigo','caja_id','calle','numero','localidad','provincia','cod_postal']
        
class CajaForm(forms.ModelForm):
    
    class Meta:
        
        model = Caja
        fields = '__all__'
        
    