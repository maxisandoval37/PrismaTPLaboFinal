from django import forms
from .models import Presupuesto


class PresupuestoForm(forms.ModelForm):
    
    
    class Meta:
        
        model = Presupuesto
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super(PresupuestoForm, self).__init__(*args, **kwargs)
        
        if self.data and self.data.get('estado') != 'APROBADO':
            self.fields.get('comentarios').required = True
        else:
            self.fields.get('comentarios').required = False