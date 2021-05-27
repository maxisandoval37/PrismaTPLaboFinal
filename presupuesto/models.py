from django.db import models
from item.models import Item
from sucursal.models import Sucursal
from django.core.exceptions import ValidationError
from django.utils import timezone
from usuario.models import Vendedor



class EstadoPresupuesto(models.Model):
    
    class opcionesEstado(models.TextChoices):
        
        EN_EVALUACION = 'EN EVALUACION'
        APROBADO = 'APROBADO'
        RECHAZADO = 'RECHAZADO'
        
    opciones = models.CharField(choices = opcionesEstado.choices, max_length=13)
    
    def __str__(self):
        return self.opciones
    
class ItemPresupuesto(models.Model):
    
    item = models.ForeignKey(Item, on_delete= models.CASCADE)       
    monto = models.DecimalField('Monto', decimal_places=2, max_digits=10, null=True)         
    presupuesto_asociado = models.ForeignKey('Presupuesto', on_delete=models.PROTECT, blank=True, null=True)
    sucursal_asociada = models.ForeignKey(Sucursal,  on_delete=models.PROTECT)
    cantidad_solicitada = models.IntegerField('Cantidad solicitada', default=0, null=True)
    
    class Meta:
        verbose_name = 'item de venta'
        verbose_name_plural = 'items de ventas'
        
    def __str__(self):
        return "Item: {}, Venta: {}".format(self.item, self.venta_asociada)    

class Presupuesto(models.Model):
    
    fecha_emision = models.DateTimeField('Fecha de emisión', auto_now_add=True)
    fecha_expiracion = models.DateTimeField('Fecha de expiración', auto_now_add=False)
    responsable_inscripto = models.BooleanField('Responsable Inscripto', default=False, blank=True, null=True)
    total = models.IntegerField('Total del presupuesto', default=0)
    estado = models.ForeignKey(EstadoPresupuesto, on_delete=models.PROTECT)
    comentarios = models.CharField('Comentarios', max_length=45,null=True, blank=True)
    sucursal_asociada = models.ForeignKey(Sucursal, on_delete=models.PROTECT)
    vendedor_asociado = models.ForeignKey(Vendedor, on_delete=models.PROTECT)
    
    def __str__(self):
        return "Fecha de emisión: {} , Fecha de expiración: {} , Estado: {} , Total: {}".format(self.fecha_emision, self.fecha_expiracion, self.estado, self.total)
    
    def clean(self):
        

        if self.estado.opciones == 'RECHAZADO' and self.comentarios == None:
            raise ValidationError('Debes completar el campo comentarios.')
        if self.estado.opciones == 'APROBADO' and self.comentarios != None:
            raise ValidationError('No es necesario que ingreses comentarios.')
        
        if (self.fecha_expiracion is None):
            raise ValidationError('El formato de la fecha es inválido')
        if timezone.now() > self.fecha_expiracion:
            raise ValidationError('La fecha no puede ser menor a la actual')
            