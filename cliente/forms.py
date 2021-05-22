from django import forms
from .models import Cliente,MedioDePago


class ClienteForm(forms.ModelForm):
    
    class Meta:
        
        model = Cliente
        fields = '__all__'


class MedioDePagoForm(forms.ModelForm):
    
    
    
    class Meta:
        model = MedioDePago
        fields = '__all__'
               