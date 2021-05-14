from django import forms
from .models import Sucursal

class SucursalForm(forms.ModelForm):
    
    codigo = forms.CharField(min_length=2 , max_length = 10, required=True)
    calle = forms.CharField( min_length =2,max_length=20, required=True)
    numero = forms.IntegerField(min_value =1000,max_value=1000, required=True)
    localidad = forms.CharField(min_length =4 , max_length=20, required=True)
    provincia = forms.CharField(min_length =4 , max_length=20, required=True)
    cod_postal = forms.IntegerField(min_value =1000 , max_value= 1000, required=True)
    
    
    
    class Meta:
        model = Sucursal
        fields = ['codigo','caja','calle','numero','localidad','cod_postal']