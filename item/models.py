from django.db import models

# Create your models here.

class Categoria(models.Model):
    
    
    id = models.AutoField(primary_key = True)
    nombre_categoria = models.CharField('nombre_categoria', max_length=50,unique = True)

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
    nombre = models.CharField('Nombre', max_length=30, blank=True, null=True)
    precio = models.FloatField('Precio',blank=True, null=True)
    stockMinimo = models.IntegerField('Stock Minimo',  default=0)
    stockSeguridad = models.IntegerField('Stock de Seguridad',  default=1)
    ubicacion = models.CharField('Ubicación', max_length=40, blank=True, null=True)
       
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, blank=True)
    unidad_de_medida = models.ForeignKey(UnidadDeMedida, on_delete=models.CASCADE, blank=True)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE, blank=True)
    
    class Meta:
        
        verbose_name = 'item'
        verbose_name_plural = 'items'
        
    def __str__(self):
        return self.nombre
    
