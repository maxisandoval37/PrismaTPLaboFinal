from .models import MedioDePago
from django import forms


class MedioDePagoForm(forms.ModelForm):
    
    
    
    class Meta:
        model = MedioDePago
        fields = '__all__'
        