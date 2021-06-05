from django.db import models
from cliente.models import Cliente,MedioDePago, CuentaCorriente
from sucursal.models import Sucursal
from usuario.models import Vendedor
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from item.models import Item
from django.db.models.signals import pre_save
from django.dispatch import receiver




class ItemVenta(models.Model):
    
    item = models.ForeignKey(Item, on_delete= models.CASCADE)       
    monto = models.DecimalField('Monto', decimal_places=2, max_digits=10, null=True)         
    venta_asociada = models.ForeignKey('Venta', on_delete=models.PROTECT, blank=True, null=True)
    sucursal_asociada = models.ForeignKey(Sucursal,  on_delete=models.PROTECT)
    cantidad_solicitada = models.IntegerField('Cantidad solicitada', default=0, null=True)
    
    class Meta:
        verbose_name = 'item de venta'
        verbose_name_plural = 'items de ventas'
        
    def __str__(self):
        return "Item: {}, Venta: {}".format(self.item, self.venta_asociada)

    
class EstadoVenta(models.Model):
    
    class opcionesVenta(models.TextChoices):
        
        CANCELADA_POR_CLIENTE = 'CANCELADA POR EL CLIENTE'
        CANCELADA_POR_SUCURSAL = 'CANCELADA POR LA SUCURSAL'
        PENDIENTE_DE_RETIRO = 'PENDIENTE DE RETIRO'
        EN_PREPARACION = 'EN PREPARACION'
        LISTA = 'LISTA'
        PAGADA = 'PAGADA'
        RETIRADA = 'RETIRADA'
        RECHAZADA = 'RECHAZADA'
        NO_RETIRADO = 'NO RETIRADA'
        
    opciones = models.CharField(max_length=25, choices=opcionesVenta.choices)
        
    def __str__(self):
        return self.opciones
    


class Venta(models.Model):
    
    fecha = models.DateTimeField('Fecha',auto_now_add=True, null=True, blank=True)
    numero_comprobante = models.AutoField('Número de comprobrante', primary_key=True)
    cliente_asociado = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    vendedor_asociado = models.ForeignKey(Vendedor, on_delete=models.PROTECT)
    sucursal_asociada = models.ForeignKey(Sucursal, on_delete=models.PROTECT)
    mediodepago = models.ForeignKey(MedioDePago, on_delete=models.PROTECT)
    cuenta_corriente = models.ForeignKey(CuentaCorriente, on_delete=models.PROTECT)
    estado = models.ForeignKey(EstadoVenta, on_delete=models.PROTECT)
    total = models.DecimalField('Total',decimal_places=2, max_digits=10, default=0)
    tipo_de_venta = models.CharField('Tipo de venta', default= 'LOCAL', null=True, blank=True, max_length=7)
    #dinero_deuda = models.DecimalField(...)
    
    
    class Meta:
        
        verbose_name = 'venta'
        verbose_name_plural = 'ventas'
        
    def __str__(self):
        return str(self.numero_comprobante)
    


    
class VentaVirtual(Venta):
    
    
    comentarios = models.CharField('Comentarios', max_length=50, null=True, blank=True)
    
    class Meta: 
        verbose_name = 'venta-virtual'
        verbose_name_plural = 'ventas-virtuales'
        
    def __str__(self):
        return "Venta virtual, número de comprobrante {}".format(self.numero_comprobante)
    
    # def clean(self):
        
          
        #if self.estado.opciones == 'PENDIENTE DE RETIRO':
        #if self.estado.opciones == 'NO RETIRADO':
               

class VentaLocal(Venta):
    
    class Meta:
        verbose_name = 'venta-local'
        verbose_name_plural= 'ventas-locales'
        
    def __str__(self):
        return "Venta local, número de comprobrante {}".format(self.numero_comprobante)

    

# def definirTipoVenta(sender, instance, **kwargs):
        
#     queryset = TipoVenta.objects.filter(opciones = 'LOCAL')
#     venta = instance
#     for id in queryset:
#         venta.tipo_de_venta_id = id.id 
#         venta.save()
#         break
        
    
# pre_save.connect(definirTipoVenta, sender = Venta)

