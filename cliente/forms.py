from django import forms
from .models import Cliente,MedioDePago, CuentaCorriente


class ClienteForm(forms.ModelForm):
    
    class Meta:
        
        model = Cliente
        fields = ['cuit','nombre','apellido','email','telefono','categoria_cliente']


class MedioDePagoForm(forms.ModelForm):
    
    
    
    class Meta:
        model = MedioDePago
        fields = '__all__'
               
class CuentaCorrienteForm(forms.ModelForm):
    
    class Meta:
        model = CuentaCorriente
        fields = ['cliente']