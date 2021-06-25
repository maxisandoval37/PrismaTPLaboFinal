from django.db import models
from cliente.models import Cliente,MedioDePago, CuentaCorriente, TipoDeMoneda
from sucursal.models import Sucursal
from usuario.models import Vendedor
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from item.models import Item
from cliente.models import Deuda
from django.db.models.signals import pre_save




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
        EN_DEUDA = 'EN DEUDA'
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
    tipo_de_moneda = models.ForeignKey(TipoDeMoneda, on_delete=models.PROTECT)
    cuenta_corriente = models.ForeignKey(CuentaCorriente, on_delete=models.PROTECT)
    estado = models.ForeignKey(EstadoVenta, on_delete=models.PROTECT)
    total_peso = models.DecimalField('Total en pesos',decimal_places=2, max_digits=10, default=0)
    total_dolar = models.DecimalField('Total en dolares',decimal_places=2, max_digits=10, default=0)
    total_euro = models.DecimalField('Total en euros',decimal_places=2, max_digits=10, default=0)
    tipo_de_venta = models.CharField('Tipo de venta', default= 'LOCAL', null=True, blank=True, max_length=7)
    monto_ingresado = models.DecimalField('Monto del cliente', default=0,decimal_places=2, max_digits=7)

    class Meta:
        
        verbose_name = 'venta'
        verbose_name_plural = 'ventas'
        
    def __str__(self):
        return str(self.numero_comprobante)
    
    def clean(self):
        
        deudas = Deuda.objects.filter(cliente_asociado_id = self.cliente_asociado)
        
        if len(deudas) >= 3:
            raise ValidationError('No es posible registrar la venta, ya que el cliente posee 3 deudas impagas.')
        
        
        try:
            if self.cliente_asociado == None:
                raise ValidationError('Error')
        except:
            raise ValidationError('Debe seleccionar un cliente asociado')
    
        try: 
            if self.mediodepago == None:
                raise ValidationError('Error')
        except:
            raise ValidationError('Debe seleccionar un medio de pago')
        
        try:
            if self.cuenta_corriente == None:
                raise ValidationError('Error')
        except:
            raise ValidationError('Debe seleccionar una cuenta corriente')
        try:
            if self.sucursal_asociada == None:
                raise ValidationError('Error')
        except:
            raise ValidationError('Debe seleccionar una sucursal asociada.')
        
        
        if self.tipo_de_moneda.opciones == 'EURO':
            if self.monto_ingresado > self.total_euro:
                raise ValidationError('No puedes ingresar un monto mayor al total de la venta.')
        if self.tipo_de_moneda.opciones == 'DOLAR':
            if self.monto_ingresado > self.total_dolar:
                raise ValidationError('No puedes ingresar un monto mayor al total de la venta.')
        if self.tipo_de_moneda.opciones == 'PESO':
            if self.monto_ingresado > self.total_peso:
                raise ValidationError('No puedes ingresar un monto mayor al total de la venta.')
        
        if self.monto_ingresado < 0:
            raise ValidationError('El monto no puede ser negativo.')
        
        deuda = Deuda.objects.filter(cliente_asociado_id = self.cliente_asociado)
        
        if len(deuda) > 3:
            raise ValidationError('No es posible registrar la venta, el cliente posee más de tres deudas.')

    
class VentaVirtual(Venta):
    
    
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

    

class Cotizacion(models.Model):
    
    moneda = models.ForeignKey(TipoDeMoneda, on_delete=models.PROTECT)
    fecha = models.DateTimeField('Fecha', auto_now_add=True)
    cotizacion = models.DecimalField('Cotización', decimal_places=2, max_digits=7)
    
    class Meta:
        verbose_name = 'cotizacion'
        verbose_name_plural = 'cotizaciones'
        
    def __str__(self):
        return "Moneda: {}, Cotización: {}".format(self.moneda, self.cotizacion)
    
    
class ComprobantePago(models.Model):
    
    fecha = models.DateTimeField('Fecha', auto_now_add=True)
    numero_venta = models.IntegerField('N° de venta')
    mediodepago = models.CharField('Método de pago', max_length=30)
    moneda = models.CharField('Tipo de moneda', max_length=30)
    vendedor = models.CharField('Vendedor Asociado', max_length=30)
    sucursal = models.CharField('Sucursal Asociada', max_length=30)
    total = models.CharField('Total de la compra', max_length= 30)
    
    class Meta:
        verbose_name = 'comprobante de pago'
        verbose_name_plural = 'comprobantes de pago'
        
    def __str__(self):
        return "Venta: {}, Total: {}".format(self.numero_venta, self.total)
    

def defaultActivoVentaLocal(sender, instance, **kwargs):
    
    
    estados = EstadoVenta.objects.all()
    if len(estados) > 0:
        
        if instance.estado_id == None:
            
            estadosQuery = EstadoVenta.objects.filter(opciones = 'EN PREPARACION')
            activo = ""
            for estado in estadosQuery:
                activo = estado.id 
            
            instance.estado_id = activo 
            
pre_save.connect(defaultActivoVentaLocal, sender = VentaLocal)
    