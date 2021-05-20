from django.db import models
from usuario.models import Usuario



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
    
    def __str__(self):
        return "Dias: " + str(self.dias) + ", Monto: "+ str(self.monto)    
    

class Cliente(models.Model):
    
    cuit = models.CharField('Cuit', max_length=11, unique=True)
    nombre = models.CharField('Nombre', max_length=20, unique=True)
    apellido = models.CharField('Apellido', max_length=20, unique=True)
    email = models.EmailField('Correo electronico', max_length=30, unique=True)
    telefono = models.CharField('Telefono', max_length=13, unique=True)
    categoria_cliente = models.ForeignKey(CategoriaCliente, on_delete=models.PROTECT)
    estado_cliente = models.ForeignKey(EstadoCliente, on_delete=models.PROTECT)
    deuda_cliente =  models.ForeignKey(Deuda, on_delete=models.PROTECT)
    vendedor_asociado = models.ForeignKey(Usuario, on_delete= models.PROTECT)
    
    def __str__(self):
        return self.nombre 
    
    
