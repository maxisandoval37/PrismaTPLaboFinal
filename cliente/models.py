from django.db import models
from usuario.models import Usuario
from django.core.exceptions import ValidationError
import re

# Create your models here.


class CategoriaCliente(models.Model):
    
    class opcionesCategoria(models.TextChoices):
        
        A = 'A'   
        B =   'B'  
        C =     'C'     
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
    
    dias = models.IntegerField('Dias', null = True)
    monto = models.FloatField('Monto', null=True)
    estado_deuda = models.ForeignKey(EstadoDeuda, on_delete= models.PROTECT)
    cliete_asociado = models.ForeignKey('Cliente', on_delete=models.PROTECT)
    
    def __str__(self):
        return "Dias: " + str(self.dias) + ", Monto: "+ str(self.monto)    


    
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
        
    
class CuentaCorriente(models.Model):
    
    numero_cuenta = models.BigIntegerField("Número de cuenta")
    cliente = models.ForeignKey('Cliente', on_delete=models.PROTECT)
    
    def __str__(self):
        return "Cliente: {}, Cuenta: {}".format(self.cliente.nombre, self.numero_cuenta)

class Cliente(models.Model):
    
    cuit = models.CharField('Cuit', max_length=11, unique=True)
    nombre = models.CharField('Nombre', max_length=20, null=True)
    apellido = models.CharField('Apellido', max_length=20, null=True)
    email = models.EmailField('Correo electronico', max_length=30, unique=True)
    telefono = models.CharField('Telefono', max_length=13, unique=True)
    categoria_cliente = models.ForeignKey(CategoriaCliente, on_delete=models.PROTECT)
    estado_cliente = models.ForeignKey(EstadoCliente, on_delete=models.PROTECT)
    
    
    def __str__(self):
        return self.cuit
    
    
    def clean(self):
        
        patron = '^[^ ][a-zA-Z ]+$'
        
        if len(self.cuit) != 11:
            raise ValidationError('El cuit debe tener exactamente 11 digitos.')
        if not self.cuit.isdigit():
            raise ValidationError('El cuit solo puede contener números.')
        if not (bool(re.search(patron,self.nombre))):
            raise ValidationError('El/los nombre solo puede contener letras.')
        if len(self.nombre) < 3 or len(self.nombre) > 20:
            raise ValidationError('El nombre debe tener entre 3 y 20 letras.')
        if not (bool(re.search(patron,self.apellido))):
            raise ValidationError('El/los apellido solo puede contener letras.')
        if len(self.apellido) < 3 or len(self.apellido) > 20:
            raise ValidationError('El apellido debe tener entre 3 y 20 letras.')
        
        if not self.telefono.isdigit():
            raise ValidationError('El telefono solo puede contener digitos.')
        if len(self.telefono) < 3 or len(self.telefono) > 13:
            raise ValidationError('El telefono debe tener entre 3 y 13 digitos.')