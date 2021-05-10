from django.shortcuts import render, redirect
from django.views.generic import CreateView,DeleteView,ListView,UpdateView
from django.urls import reverse_lazy
from .forms import SucursalForm
from .models import Sucursal 


class SucursalList(ListView):
    model = Sucursal
    template_name = 'index.html'

class SucursalCreate(CreateView):
    model = Sucursal
    form_class = SucursalForm
    template_name = 'crear_sucursal.html'
    success_url = reverse_lazy('index')

class SucursalUpdate(UpdateView):
    model = Sucursal
    form_class = SucursalForm
    template_name = 'crear_sucursal.html'
    success_url = reverse_lazy('index')

class SucursalDelete(DeleteView):
    model = Sucursal
    template_name = 'verificacion.html'
    success_url = reverse_lazy('index')







