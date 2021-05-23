from django import forms
from .models import Cliente,MedioDePago, CuentaCorriente


class ClienteForm(forms.ModelForm):
    
    class Meta:
        
        model = Cliente
        fields = '__all__'


class MedioDePagoForm(forms.ModelForm):
    
    
    
    class Meta:
        model = MedioDePago
        fields = '__all__'
               
class CuentaCorrienteForm(forms.ModelForm):
    
    class Meta:
        model = CuentaCorriente
        fields = '__all__'