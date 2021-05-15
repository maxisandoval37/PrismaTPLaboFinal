from django import forms
from .models import Sucursal, Caja

class SucursalForm(forms.ModelForm):
    
    codigo = forms.CharField(min_length=2 , max_length = 10, required=True)
    calle = forms.CharField( min_length =2,max_length=20, required=True)
    numero = forms.IntegerField(min_value =1000,max_value=9999, required=True)
    localidad = forms.CharField(min_length =4 , max_length=20, required=True)
    provincia = forms.CharField(min_length =4 , max_length=20, required=True)
    cod_postal = forms.IntegerField(min_value =1000 , max_value= 9999, required=True)
    
    
    
    class Meta:
        model = Sucursal
        fields = ['codigo','caja','calle','numero','localidad','provincia','cod_postal']
        
class CajaForm(forms.ModelForm):
    
    codigo = forms.CharField(min_length=2, max_length=4 , required=True)
    saldo_disponible = forms.DecimalField(min_value=10, max_value=999999999,required=True)
    egresos = forms.DecimalField(min_value=10, max_value=999999999,required=True)
    ingresos = forms.DecimalField( min_value=10, max_value=999999999,required=True)
    saldo_inicial = forms.DecimalField( min_value=10, max_value=999999999,required=True)
    saldo_final = forms.DecimalField( min_value=10, max_value=999999999,required=True)
    
    
    class Meta:
        
        model = Caja
        fields = '__all__'
        
    """      
    def __init__(self, *args, **kwargs):
        super(CajaForm, self).__init__(*args, **kwargs)
        
        self.fields["saldo_disponible"].error_messages={"Ingrese un saldo menor a 9 cifras"}
        self.fields["egresos"].error_messages={"Ingrese un monto de egresos menor a 9 cifras"}
        self.fields["ingresos"].error_messages={"Ingrese un monto de ingresos menor a 9 cifras"}
        self.fields["saldo_inicial"].error_messages={"Ingrese un saldo inicial menor a 9 cifras"}
        self.fields["saldo_final"].error_messages={"Ingrese un saldo final menor a 9 cifras"} """