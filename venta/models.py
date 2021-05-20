from django.db import models
from cliente.models import Cliente
from usuario.models import Usuario
from sucursal.models import Sucursal
from item.models import Item
from mediodepago.models import MedioDePago
from django.utils.translation import gettext_lazy as _
# Create your models here.

class Venta(models.Model):
    
    fecha = models.DateTimeField('Fecha',auto_now_add=True, null=True)
    numero_comprobante = models.CharField('Número de comprobrante', max_length=25, unique=True)
    monto = models.FloatField('Monto', null=True)
    cliente_asociado = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    vendedor_asociado = models.ForeignKey(Usuario, on_delete=models.PROTECT)
    sucursal_asociada = models.ForeignKey(Sucursal, on_delete=models.PROTECT)
    item_asociado = models.ForeignKey(Item, on_delete= models.PROTECT)
    mediodepago = models.ForeignKey(MedioDePago, on_delete=models.PROTECT)
    
    class Meta:
        
        
        verbose_name = 'venta'
        verbose_name_plural = 'ventas'
        
    def __str__(self):
        return self.numero_comprobante
    
    
    
class EstadoVentaVirtual(models.Model):
    
    class opcionesVentaVirtual(models.TextChoices):
        
        CANCELADA_POR_CLIENTE = 'CANCELADO POR EL CLIENTE'
        CANCELADA_POR_SUCURSAL = 'CANCELADO POR LA SUCURSAL'
        PENDIENTE = 'PENDIENTE'
        EN_PREPARACION = 'EN PREPARACIÓN'
        LISTA = 'LISTA'
        RETIRADA = 'RETIRADA'
        RECHAZADA = 'RECHAZADA'
        
    opciones = models.CharField(max_length=25, choices=opcionesVentaVirtual.choices)
        
    def __str__(self):
        return self.opciones
    
    
class VentaVirtual(Venta):
    
    estado = models.ForeignKey(EstadoVentaVirtual, on_delete=models.PROTECT)
    comentarios = models.CharField('Comentarios', max_length=50, null=True, blank=True)
    
    class Meta: 
        verbose_name = 'venta-virtual'
        verbose_name_plural = 'ventas-virtuales'
        
    def __str__(self):
        return "Venta virtual, número de comprobrante {}".format(self.numero_comprobante)
    

class VentaLocal(Venta):
    
    class Meta:
        verbose_name = 'venta-local'
        verbose_name_plural= 'ventas-locales'
        
    def __str__(self):
        return "Venta local, número de comprobrante {}".format(self.numero_comprobante)



    