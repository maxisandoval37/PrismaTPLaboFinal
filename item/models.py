from django.shortcuts import redirect
from django.db import models
from sucursal.models import Sucursal
from django.db.models.signals import post_save
from proveedor.models import Proveedor

# Create your models here.

class SubCategoria(models.Model):
    
    nombre= models.CharField('Nombre', max_length=30, unique = True)   
    nombre_categoria = models.ForeignKey('Categoria', on_delete=models.PROTECT)
    class Meta:
        
        verbose_name = 'subcategoria'
        verbose_name_plural = 'subcategorias'
        
    def __str__(self):
        return self.nombre


class Categoria(models.Model):
    
    nombre_categoria = models.CharField('Nombre', max_length=30,unique = True)
    prov_preferido = models.ForeignKey(Proveedor, on_delete=models.PROTECT, null = True, blank=True)
    
    class Meta:

        verbose_name = 'categoria'
        verbose_name_plural = 'categorias'

    def __str__(self):
        
        return self.nombre_categoria
 

    
class UnidadDeMedida(models.Model):
    
    
    id = models.AutoField(primary_key = True)
    unidad_de_medida = models.CharField('tipo_de_unidad', max_length=10,unique = True)

    class Meta:

        verbose_name = 'unidad_de_medida'
        verbose_name_plural = 'unidades_de_medida'

    def __str__(self):
       
        return self.unidad_de_medida
    
class Estado(models.Model):
    
    id = models.AutoField(primary_key = True)
    estado = models.CharField('Estado', max_length=20,unique = True)
    
    class Meta:

        verbose_name = 'estado'
        verbose_name_plural = 'estados'

    def __str__(self):
        
        return self.estado

class Item(models.Model):
    
    id = models.AutoField(primary_key = True)
    nombre = models.CharField('Nombre', max_length=30, unique = True)
    precio = models.FloatField('Precio', null=True)
    descripcion = models.CharField('Descripción', max_length= 50, null=True, blank=True)
    stockMinimo = models.IntegerField('Stock Minimo',  default=0)
    stockSeguridad = models.IntegerField('Stock de Seguridad',  default=1)
    ubicacion = models.CharField('Ubicación', max_length=40, blank=True, null=True)
    ultima_modificacion = models.DateTimeField('Ultima Modificación', blank=True, null=True)
    repo_por_lote = models.BooleanField('Reposición por Lote', blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, blank=True, null=True)
    subcategoria = models.ForeignKey(SubCategoria, on_delete=models.PROTECT, blank=True, null=True)
    cantidad  = models.IntegerField("Cantidad", default = 0)
    alerta = models.BooleanField(default= False)
    
    
    unidad_de_medida = models.ForeignKey(UnidadDeMedida, on_delete=models.PROTECT)
    estado = models.ForeignKey(Estado, on_delete=models.PROTECT)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.PROTECT)
    
    
    class Meta:
        
        verbose_name = 'item'
        verbose_name_plural = 'items'
        
    def __str__(self):
        return self.nombre




""" def alertaStock(sender, instance, **kwargs):  
    item_id = instance.id 
    item = Item.objects.get(id = item_id)
    print(item.cantidad)
    if item.stockMinimo == 0:
        
        Item.objects.filter(id = item.id).update(alerta = )
    else:
        item.alerta = False
        item.save()
        return redirect('index')
    
    
    
        
    
post_save.connect(alertaStock, sender=Item)
   """