from django import forms
from .models import Item


class ItemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ItemForm, self).__init__(*args,**kwargs)
        self.fields['nombre'].widget.attrs['class'] = 'form-user'
        self.fields['nombre'].widget.attrs['placeholder'] = 'Nombre de item'
        self.fields['precio'].widget.attrs['class'] = 'form-user'
        self.fields['precio'].widget.attrs['placeholder'] = 'Precio'
        self.fields['ubicacion'].widget.attrs['class'] = 'form-user'
        self.fields['ubicacion'].widget.attrs['placeholder'] = 'Ubicación'
        self.fields['categoria'].widget.attrs['class'] = 'form-user'
        self.fields['categoria'].widget.attrs['placeholder'] = 'Categoria'
        self.fields['unidad_de_medida'].widget.attrs['class'] = 'form-user'
        self.fields['unidad_de_medida'].widget.attrs['placeholder'] = 'Unidad de medida'
        self.fields['estado'].widget.attrs['class'] = 'form-user'
        self.fields['estado'].widget.attrs['placeholder'] = 'Estado'
        self.fields['repo_por_lote'].widget.attrs['class'] = 'form-user'
        self.fields['repo_por_lote'].widget.attrs['placeholder'] = 'Reposición por lote'
    
    
    class Meta:
        
        model = Item
        fields = ['nombre','precio','ubicacion','categoria','unidad_de_medida','repo_por_lote','estado','sucursal']
        
""" 
        self.fields['stockMinimo'].widget.attrs['class'] = 'form-user'
        self.fields['stockMinimo'].widget.attrs['placeholder'] = 'Stock Minimo'
        self.fields['stockSeguridad'].widget.attrs['class'] = 'form-user'
        self.fields['stockSeguridad'].widget.attrs['placeholder'] = 'Stock de seguridad' 
        """