from django.db import models
from item.models import Item
from sucursal.models import Sucursal
from django.core.exceptions import ValidationError

# Create your models here.
class EstadoPresupuesto(models.Model):
    
    class opcionesEstado(models.TextChoices):
        
        APROBADO = 'APROBADO'
        RECHAZADO = 'RECHAZADO'
        
    opciones = models.CharField(choices = opcionesEstado.choices, max_length=9)
    
    def __str__(self):
        return self.opciones

class Presupuesto(models.Model):
    
    fecha_emision = models.DateTimeField('Fecha de emisión', auto_now_add=True)
    fecha_expiracion = models.DateTimeField('Fecha de expiración', auto_now_add=False)
    responsable_inscripto = models.BooleanField('Responsable Inscripto', default=False, blank=True, null=True)
    total = models.IntegerField('Total del presupuesto', null=True)
    estado = models.ForeignKey(EstadoPresupuesto, on_delete=models.PROTECT)
    comentarios = models.CharField('Comentarios', max_length=45,null=True, blank=True)
    items = models.ForeignKey(Item, on_delete=models.PROTECT)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.PROTECT)
    
    def __str__(self):
        return "Fecha de emisión: {} , Fecha de expiración: {} , Estado: {} , Total: {}".format(self.fecha_emision, self.fecha_expiracion, self.estado, self.total)
    
    def clean(self):
        if self.total < 0:
            raise ValidationError('El total no puede ser negativo.')

        if self.estado.opciones == "RECHAZADO" and self.comentarios == None:
            raise ValidationError('Debes completar el campo comentarios.')
        if self.estado.opciones == "APROBADO" and self.comentarios != None:
            raise ValidationError('No es necesario que ingreses comentarios.')
      
            