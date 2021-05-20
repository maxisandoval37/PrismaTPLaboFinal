from django.db import models
from item.models import Item
from sucursal.models import Sucursal

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
    fecha_expiracion = models.DateTimeField('Fecha de expiración', auto_now_add=True)
    responsable_inscripto = models.BooleanField('Responsable Inscripto', default=False)
    total = models.IntegerField('Total del presupuesto', null=True)
    estado = models.ForeignKey(EstadoPresupuesto, on_delete=models.PROTECT)
    comentarios = models.CharField('Comentarios', max_length=45,blank=True, null=True)
    items = models.ForeignKey(Item, on_delete=models.PROTECT)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.PROTECT)
    
    def __str__(self):
        return "Fecha de emisión: {} , Fecha de expiración: {} , Estado: {} , Total: {}".format(self.fecha_emision, self.fecha_expiracion, self.estado, self.total)
    
    