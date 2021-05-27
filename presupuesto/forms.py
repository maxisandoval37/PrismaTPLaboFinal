from typing import AbstractSet
from django import forms
from .models import Presupuesto


class PresupuestoForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(PresupuestoForm, self).__init__(*args,**kwargs)
        self.fields['fecha_expiracion'].widget.attrs['class'] = 'form-user'
        self.fields['fecha_expiracion'].widget.attrs['placeholder'] = 'Dia/Mes/Año'
    
    
    class Meta:
        
        model = Presupuesto
        fields = ['responsable_inscripto','fecha_expiracion','estado','sucursal_asociada','vendedor_asociado','comentarios']
        
         
        
        