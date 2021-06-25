from django.db import models
from django.core.exceptions import ValidationError
import re
from django.db.models.signals import pre_save
from django.db.models.enums import TextChoices

# Create your models here.


class CategoriaCliente(models.Model):
    
    class opcionesCategoria(models.TextChoices):
        
        A = 'A'   
        B = 'B'  
        C = 'C'     
    opciones = models.CharField(choices = opcionesCategoria.choices, max_length=1)
    
    def __str__(self):
        return self.opciones
    
    
class EstadoCliente(models.Model):
    
    class opcionesEstado(models.TextChoices):
        
        ACTIVO = 'ACTIVO'
        INACTIVO = 'INACTIVO'
        DEUDOR =    'DEUDOR'
        INCOBRABLE =  'INCOBRABLE'
        
    opciones = models.CharField(choices = opcionesEstado.choices, max_length=10)
    
    def __str__(self):
        return self.opciones
    
class EstadoDeuda(models.Model):
    
    class opcionesEstado(models.TextChoices):
        
        PAGA = 'PAGA'
        IMPAGA = 'IMPAGA'
        
    opciones = models.CharField(choices= opcionesEstado.choices, max_length=6)
    
    def __str__(self):
        return self.opciones
        
    
class Deuda(models.Model):
    
    fecha = models.DateTimeField('Fecha', auto_now_add=True)
    monto = models.FloatField('Monto', null=True)
    estado_deuda = models.ForeignKey(EstadoDeuda, on_delete= models.PROTECT)
    cliente_asociado = models.ForeignKey('Cliente', on_delete=models.PROTECT)
    numero_venta = models.BigIntegerField('Número de venta')
    
    def __str__(self):
        return "Dias: " + str(self.fecha) + ", Monto: "+ str(self.monto)    


    
class MedioDePago(models.Model):  
     
    cliente = models.ForeignKey('Cliente', on_delete= models.PROTECT)
    
    class opcionesDePago(models.TextChoices):
        
        DEBITO = 'DÉBITO'
        CREDITO =  'CRÉDITO'
        TRANSFERENCIA = 'TRANSFERENCIA'
        MERCADOPAGO =  'MERCADOPAGO'
        EFECTIVO =  'EFECTIVO'
        CHEQUE = 'CHEQUE'
    
    opciones = models.CharField(choices= opcionesDePago.choices, max_length=13)
    
    def __str__(self):
        return self.opciones
        
    def clean(self):
        
        medios_de_pagos = MedioDePago.objects.filter(cliente = self.cliente)
        if len(medios_de_pagos) == 0 and self.cliente.nombre == 'CONSUMIDOR FINAL':
            if self.opciones != 'EFECTIVO':
                raise ValidationError('El consumidor final solo puede pagar en efectivo.')
            
        for medios in medios_de_pagos:
            
            if self.opciones == medios.opciones:
                raise ValidationError('No es posible añadir un medio de pago ya registrado.')
                
            if self.cliente.nombre == 'CONSUMIDOR FINAL' and self.opciones != 'EFECTIVO':
                raise ValidationError('El consumidor final solo puede pagar con efectivo.')
            
class TipoDeMoneda(models.Model):
    
    class opcionesTipo(models.TextChoices):
        
        EURO = 'EURO'
        DOLAR = 'DOLAR'
        PESO = 'PESO'
        
    opciones = models.CharField(choices = opcionesTipo.choices, max_length= 5)
    
    def __str__(self):
        return self.opciones
    
    def clean(self):
        
        monedas = TipoDeMoneda.objects.all()
        for moneda in monedas:
            
            if self.opciones == moneda.opciones:
                raise ValidationError('No es posible añadir un tipo de moneda ya registrado.')

class EstadoCuentaCorriente(models.Model):
    
    class opcionesEstado(TextChoices):
        
        ACTIVA = 'ACTIVA'
        INACTIVA = 'INACTIVA'
        
    opciones = models.CharField(choices = opcionesEstado.choices, max_length= 8)
    
    def __str__(self):
        return self.opciones

   
class CuentaCorriente(models.Model):
    
    numero_cuenta = models.AutoField("Número de cuenta", primary_key=True)
    cliente = models.ForeignKey('Cliente', on_delete=models.PROTECT)
    estado = models.ForeignKey(EstadoCuentaCorriente, on_delete=models.PROTECT)
    
    def __str__(self):
        return "Cliente: {}, Cuenta: {}".format(self.cliente.nombre, self.numero_cuenta)

    def clean(self):
        
        if self.cliente.estado_cliente.opciones == 'INACTIVO':
            raise ValidationError('No puedes registrar una cuenta corriente para un cliente inactivo.')
        
        cuentas_corriente = CuentaCorriente.objects.all()
        cuenta_corriente = CuentaCorriente.objects.filter(cliente = self.cliente)
        contador = 0
        
        for cuenta in cuenta_corriente:
            contador += 1
            
        for cuenta in cuentas_corriente:
            

            if self.cliente.nombre == 'CONSUMIDOR FINAL' and contador == 1:
                raise ValidationError('El consumidor final sólo puede tener una cuenta corriente genérica.')
            
            
class Cliente(models.Model):
    
    cuit = models.CharField('Cuit', max_length=11, unique=True)
    nombre = models.CharField('Nombre', max_length=20, null=True)
    apellido = models.CharField('Apellido', max_length=20, null=True)
    email = models.EmailField('Correo electronico', max_length=30, unique=True)
    telefono = models.CharField('Telefono', max_length=13, unique=True)
    categoria_cliente = models.ForeignKey(CategoriaCliente, on_delete=models.PROTECT)
    estado_cliente = models.ForeignKey(EstadoCliente, on_delete=models.PROTECT, null=True)
    
    
    def __str__(self):
        return self.cuit
    
    
    def clean(self):
        
        clientes = Cliente.objects.all() 
        
        for cliente in clientes:
            if self.cuit == cliente.cuit and self.id != cliente.id:
                raise ValidationError('Ya existe un cliente con el cuit ingresado.')
            
        for char in self.nombre:
            
            if not char.isalpha and char != " ":
                raise ValidationError("El nombre solo puede contener letras y espacios.")
            
        for char in self.apellido:
        
            if not char.isalpha and char != " ":
                raise ValidationError("El apellido solo puede contener letras y espacios.")   
    
        
        if len(self.cuit) != 11:
            raise ValidationError('El cuit debe tener exactamente 11 digitos.')
        if not self.cuit.isdigit():
            raise ValidationError('El cuit solo puede contener números.')
        
        if len(self.nombre) < 3 or len(self.nombre) > 20:
            raise ValidationError('El nombre debe tener entre 3 y 20 letras.')
        
        if len(self.apellido) < 3 or len(self.apellido) > 20:
            raise ValidationError('El apellido debe tener entre 3 y 20 letras.')
        
        if not self.telefono.isdigit():
            raise ValidationError('El telefono solo puede contener digitos.')
        if len(self.telefono) < 3 or len(self.telefono) > 13:
            raise ValidationError('El telefono debe tener entre 3 y 13 digitos.')
        
        
def defaultActivoCliente(sender, instance, **kwargs):
    
   
    estados = EstadoCliente.objects.all()
    if len(estados) > 0:
        if instance.estado_cliente  == None:
            
            estadosQuery = EstadoCliente.objects.filter(opciones = 'ACTIVO')
            activo = ""
            for estado in estadosQuery:
                activo = estado.id 
            
            instance.estado_cliente_id = activo
            
           
pre_save.connect(defaultActivoCliente, sender = Cliente)

def defaultActivoCuentaCorriente(sender, instance, **kwargs):
    
    
    estados = EstadoCuentaCorriente.objects.all()
    if len(estados) > 0:
        
        if instance.estado_id == None:
           
            estadosQuery = EstadoCuentaCorriente.objects.filter(opciones = 'ACTIVA')
            activo = ""
            for estado in estadosQuery:
                activo = estado.id 
            
            instance.estado_id = activo
           
            
pre_save.connect(defaultActivoCuentaCorriente, sender = CuentaCorriente)