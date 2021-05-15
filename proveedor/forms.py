from django import forms
from .models import Proveedor


class ProveedorForm(forms.ModelForm):
    
    cuit = forms.CharField(min_length =11 ,max_length=11, required=True)
    razon_social = forms.CharField(min_length =4 , max_length = 20, required=True)
    email = forms.EmailField(min_length =6 , max_length=30, required=True)
    telefono = forms.IntegerField(min_value= 100 , max_value=9999999999999, required=True)
    calle = forms.CharField(min_length =2 , max_length=4)
    numero = forms.IntegerField(min_value =10, max_value=9999)
    localidad = forms.CharField(min_length =4 , max_length=20)
    provincia = forms.CharField(min_length =4 , max_length=20)
    cod_postal = forms.IntegerField(min_value =1000 , max_value= 9999)
    
    
    class Meta:
        model = Proveedor
        fields = '__all__'
        
        