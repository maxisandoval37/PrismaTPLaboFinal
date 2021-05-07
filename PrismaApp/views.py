from django.shortcuts import render, redirect
from .models import *
from .forms import UserRegisterForm
from django.contrib import messages



# Create your views here.


def home(request):
    
    return render(request, "PrismaApp/home.html")

def registro(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        #formUser = UsuarioForm(request.POST)   
        if form.is_valid():
           
            form.save()
            #formUser.save()
            username = form.cleaned_data['username']
            messages.success(request, f'Usuario {username} creado')
            return redirect('login')
    else:
        form = UserRegisterForm()
        #formUser = UsuarioForm()
    context = {'form': form}
        
    return render(request, 'PrismaApp/registro.html', context)
    

    
    