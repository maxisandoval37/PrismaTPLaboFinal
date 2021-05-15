from django import forms
from .models import Proveedor


class ProveedorForm(forms.ModelForm):
    
    cuit = forms.IntegerField(min_value =1000000000 ,max_value=10000000000, required=True)
    razon_social = forms.CharField(min_length =4 , max_length = 20, required=True)
    email = forms.EmailField(min_length =6 , max_length=30, required=True)
    telefono = forms.IntegerField(min_value= 100 , max_value=1000000000000, required=True)
    calle = forms.CharField(min_length =2 , max_length=4)
    numero = forms.IntegerField(min_value =10, max_value=1000)
    localidad = forms.CharField(min_length =4 , max_length=20)
    provincia = forms.CharField(min_length =4 , max_length=20)
    cod_postal = forms.IntegerField(min_value =1000 , max_value= 1000)
    
    
    class Meta:
        model = Proveedor
        fields = '__all__'
        
        