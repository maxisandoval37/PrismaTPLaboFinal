from django import forms
from .models import Item, Pedidos


class ItemForm(forms.ModelForm):
    
    
    def __init__(self, *args, **kwargs):
        super(ItemForm, self).__init__(*args,**kwargs)
        self.fields['nombre'].widget.attrs['class'] = 'form-user'
        self.fields['nombre'].widget.attrs['placeholder'] = 'Nombre de item'
        self.fields['precio'].widget.attrs['class'] = 'form-user'
        self.fields['precio'].widget.attrs['placeholder'] = 'Precio'
        self.fields['ubicacion'].widget.attrs['class'] = 'form-user'
        self.fields['ubicacion'].widget.attrs['placeholder'] = 'Ubicación'
        self.fields['descripcion'].widget.attrs['class'] = 'form-user'
        self.fields['descripcion'].widget.attrs['placeholder'] = 'Descripción'
        self.fields['categoria'].widget.attrs['class'] = 'form-user'
        self.fields['categoria'].widget.attrs['placeholder'] = 'Categoria'
        self.fields['subcategoria'].widget.attrs['class'] = 'form-user'
        self.fields['subcategoria'].widget.attrs['placeholder'] = 'Sub-categoria'
        self.fields['unidad_de_medida'].widget.attrs['class'] = 'form-user'
        self.fields['unidad_de_medida'].widget.attrs['placeholder'] = 'Unidad de medida'
        self.fields['estado'].widget.attrs['class'] = 'form-user'
        self.fields['estado'].widget.attrs['placeholder'] = 'Estado'
        self.fields['repo_por_lote'].widget.attrs['class'] = 'form-user'
        self.fields['repo_por_lote'].widget.attrs['placeholder'] = 'Reposición por lote'
    
    
    class Meta:
        
        model = Item
        fields = ['nombre','precio','ubicacion','descripcion','categoria','subcategoria','unidad_de_medida','repo_por_lote','estado','sucursal']
        

