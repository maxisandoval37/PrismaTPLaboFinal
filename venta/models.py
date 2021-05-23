from django.db import models
from cliente.models import Cliente,MedioDePago, CuentaCorriente
from sucursal.models import Sucursal
from usuario.models import Vendedor
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from item.models import Item
#from sucursal.models import Caja



class ItemVenta(models.Model):
    
    item = models.ForeignKey(Item, on_delete= models.CASCADE)       
    monto = models.DecimalField('Monto', decimal_places=2, max_digits=10, null=True)         
    venta_asociada = models.ForeignKey('Venta', on_delete=models.PROTECT, blank=True, null=True)
    sucursal_asociada = models.ForeignKey(Sucursal,  on_delete=models.PROTECT)
    
    class Meta:
        verbose_name = 'item de venta'
        verbose_name_plural = 'items de ventas'
        
    def __str__(self):
        return "Item: {}, Venta: {}".format(self.item, self.venta_asociada)

    def clean(self):
        
        if self.item.cantidad == 0:
            raise ValidationError('No hay stock del item solicitado.') 
        
      #  if self.item.precio != self.venta_asociada.monto:
     #       raise ValidationError("El precio del item es: "+str(self.item.precio))
        
        if self.item.precio >= 10000:
            raise ValidationError("El cliente debe ser registrado para finalizar la venta.")
        
        if self.item.cantidad < self.venta_asociada.cantidad_solicitada:
            raise ValidationError('No disponemos de la cantidad solicitada. Stock actual: ' + str(self.item.cantidad))
                


# Create your models here.

class Venta(models.Model):
    
    fecha = models.DateTimeField('Fecha',auto_now_add=True, null=True, blank=True)
    numero_comprobante = models.CharField('Número de comprobrante', max_length=25, unique=True)
    cliente_asociado = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    vendedor_asociado = models.ForeignKey(Vendedor, on_delete=models.PROTECT)
    sucursal_asociada = models.ForeignKey(Sucursal, on_delete=models.PROTECT)
    mediodepago = models.ForeignKey(MedioDePago, on_delete=models.PROTECT)
    cantidad_solicitada = models.IntegerField('Cantidad solicitada', default=0, null=True)
    cuenta_corriente = models.ForeignKey(CuentaCorriente, on_delete=models.PROTECT)
    
    
    
    class Meta:
        
        verbose_name = 'venta'
        verbose_name_plural = 'ventas'
        
    def __str__(self):
        return self.numero_comprobante
    
    def clean(self):
        
        if self.monto <= 0:
            raise ValidationError('Debe ingresar un monto valido.')
        
       
        
        if self.cantidad_solicitada < 0:
            raise ValidationError('La cantidad no puede ser negativa.') 
    
       
        if self.cantidad_solicitada == None or self.cantidad_solicitada <= 0:
            raise ValidationError('Debe ingresar una cantidad para solicitar.')
        
        
        
                
        # queryset = Item.objects.filter(id = self.item_asociado.id, sucursal = self.sucursal_asociada)
        
        # for item in queryset:
        #     if item.cantidad < self.cantidad_solicitada:
        #         raise ValidationError('No disponemos de la cantidad solicitada. Stock actual: ' + str(item.cantidad)) 
            
        #     else:
        #         item.cantidad = item.cantidad - self.cantidad_solicitada
        #         item.save()
        #         break
            
                
    
  
    
class EstadoVentaVirtual(models.Model):
    
    class opcionesVentaVirtual(models.TextChoices):
        
        CANCELADA_POR_CLIENTE = 'CANCELADO POR EL CLIENTE'
        CANCELADA_POR_SUCURSAL = 'CANCELADO POR LA SUCURSAL'
        PENDIENTE_DE_RETIRO = 'PENDIENTE DE RETIRO'
        EN_PREPARACION = 'EN PREPARACIÓN'
        LISTA = 'LISTA'
        RETIRADA = 'RETIRADA'
        RECHAZADA = 'RECHAZADA'
        NO_RETIRADO = 'NO RETIRADO'
        
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
    
    def clean(self):
        
        if self.item_asociado.cantidad == 0:
            raise ValidationError('No hay stock del item solicitado.')
        
        #if self.estado.opciones == 'PENDIENTE DE RETIRO':
        #if self.estado.opciones == 'NO RETIRADO':
          
            

class VentaLocal(Venta):
    
    class Meta:
        verbose_name = 'venta-local'
        verbose_name_plural= 'ventas-locales'
        
    def __str__(self):
        return "Venta local, número de comprobrante {}".format(self.numero_comprobante)

    
    # def clean(self):
        
    #     cajas = Caja.objects.filter(sucursal_id = self.sucursal_asociada.id)
            
    #     for caja in cajas:   
    #         if caja.saldo_disponible < self.monto:
    #             raise ValidationError('Saldo insuficiente en las cajas de la sucursal: '+ str(self.sucursal_asociada))
            
    #         else:
    #             caja.saldo_disponible = caja.saldo_disponible - self.monto
    #             caja.save()
    #             break        
       
       
