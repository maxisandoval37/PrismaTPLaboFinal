from django.db import models
from django.core.exceptions import ValidationError

""" class Efectivo(models.Model):
    cantidad = models.CharField('Cantidad', max_length=10)
    
    def __str__(self):
        return "Cantidad: "+ self.cantidad
    
    
class Transferencia(models.Model):
    
    cbu = models.CharField('CBU/CVU', max_length=30, unique=True)
    cuit = models.CharField('Cuit', max_length= 11, unique=True)
    titular = models.CharField('Titular', max_length=20, unique=True)
    
    def __str__(self):
        return "CBU: "+ self.cbu + " Cuit: "+ self.cuit + "  Titular: "+self.titular

class Cheque(models.Model):
    
    titular = models.CharField('Titular', max_length=20, unique=True)
    cuit = models.CharField('Cuit',max_length= 11, unique=True)
    numero_de_orden = models.CharField('Número de orden', max_length=25)
    banco = models.CharField('Banco', max_length=15)
    
    def __str__(self):
        return "Titular: "+self.titular +" Cuit: "+self.cuit+" Número de orden: "+ self.numero_de_orden+" Banco: "+ self.banco

class TipoTarjeta(models.Model):
    
    nombre = models.CharField('Débito o Crédito', max_length=10)
    
    def __str__(self):
        return "Tipo de tarjeta: " +self.nombre """
""" 
class Tarjeta(models.Model):
    
    numero = models.CharField('Número de tarjeta', max_length=30,unique=True)
    fecha_vencimiento = models.DateField('Vecha de vencimiento')
    titular = models.CharField('Titular', max_length=20, unique=True)
    cod_seguridad = models.CharField('Código de seguridad',max_length=5)
    tipo = models.ForeignKey(TipoTarjeta, on_delete=models.PROTECT)
    
    def __str__(self):
        return "Número: "+self.numero +" Titular: "+ self.titular
    
class MercadoPago(models.Model):
    
    email = models.EmailField('Correo electronico', max_length=30, unique=True)
    
    def __str__(self):
        return "Correo electronico: "+self.email """

class TipoDePago(models.Model):
    
    nombre = models.CharField("Tipo de pago", max_length=20)
    
    def clean(self):
        
        if len(self.nombre) < 6 and  len(self.nombre) > 20:
            raise ValidationError('El tipo de pago debe tener entre 6 y 20 letras.')
    
    def __str__(self):
        return self.nombre
    
    
class MedioDePago(models.Model):  
     
    tipo_de_pago = models.ForeignKey(TipoDePago, on_delete=models.PROTECT)
    
    def __str__(self):
        return self.tipo_de_pago.nombre
    
    
    class Meta:
        verbose_name = 'mediodepago'
        verbose_name_plural = 'mediosdepago'
        
        