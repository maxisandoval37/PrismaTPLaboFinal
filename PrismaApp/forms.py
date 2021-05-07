from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegisterForm(UserCreationForm):
    
    
    password1 = forms.CharField(label='Contraseña',max_length=30, widget= forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar Contraseña',max_length=30, widget= forms.PasswordInput)
   
   
    
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        
        help_texts ={k: "" for k in fields} 
        

