from django.shortcuts import redirect
from django.db import models
from sucursal.models import Sucursal
from django.db.models.signals import post_save
from proveedor.models import Proveedor
from django.core.exceptions import ValidationError
# Create your models here.


class SubCategoria(models.Model):

    nombre = models.CharField('Nombre', max_length=30, unique=True)
    nombre_categoria = models.ForeignKey('Categoria', on_delete=models.PROTECT)

    class Meta:

        verbose_name = 'subcategoria'
        verbose_name_plural = 'subcategorias'

    def clean(self):

        if len(self.nombre) < 4 and len(self.nombre) > 30:
            raise ValidationError('El nombre debe tener entre 4 y 30 letras.')

    def __str__(self):
        return self.nombre


class Categoria(models.Model):

    nombre_categoria = models.CharField('Nombre', max_length=30, unique=True)
    prov_preferido = models.ForeignKey(
        Proveedor, on_delete=models.PROTECT, null=True, blank=True)

    def clean(self):
        
        if len(self.nombre_categoria) < 4 and len(self.nombre_categoria) > 30:
            raise ValidationError(
                'El nombre de la categoria debe tener entre 4 y 30 letras.')

    class Meta:

        verbose_name = 'categoria'
        verbose_name_plural = 'categorias'

    def __str__(self):

        return self.nombre_categoria


class UnidadDeMedida(models.Model):

    id = models.AutoField(primary_key=True)
    unidad_de_medida = models.CharField(
        'tipo_de_unidad', max_length=10, unique=True)

    def clean(self):

        if not self.unidad_de_medida.isalpha():
            raise ValidationError(
                'La unidad de medida solo puede contener letras, no se admiten espacios.')
        if len(self.unidad_de_medida) < 2 and len(self.unidad_de_medida) > 10:
            raise ValidationError(
                'La unidad de medida debe tener entre 2 y 10 letras.')

    class Meta:

        verbose_name = 'unidad_de_medida'
        verbose_name_plural = 'unidades_de_medida'

    def __str__(self):

        return self.unidad_de_medida


class Estado(models.Model):

    id = models.AutoField(primary_key=True)
    estado = models.CharField('Estado', max_length=15, unique=True)

    def clean(self):
        if not self.estado.isalpha():
            raise ValidationError('El estado solo puede contener letras, no se admiten espacios.')
        if len(self.estado) < 4 and len(self.estado) > 15:
            raise ValidationError('El estado debe tener entre 4 y 15 letras.')

    class Meta:

        verbose_name = 'estado'
        verbose_name_plural = 'estados'

    def __str__(self):

        return self.estado


class Item(models.Model):

    id = models.AutoField(primary_key=True)
    nombre = models.CharField('Nombre', max_length=20, unique=True)
    precio = models.FloatField('Precio')
    descripcion = models.CharField('Descripción', max_length=50, null=True, blank=True)
    stockMinimo = models.IntegerField('Stock Minimo',  default=0)
    stockSeguridad = models.IntegerField('Stock de Seguridad',  default=1)
    ubicacion = models.CharField('Ubicación', max_length=15)
    ultima_modificacion = models.DateTimeField('Ultima Modificación', blank=True, null=True)
    repo_por_lote = models.BooleanField('Reposición por Lote')
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    subcategoria = models.ForeignKey(SubCategoria, on_delete=models.PROTECT)
    cantidad = models.IntegerField("Cantidad", default=0)
    solicitud = models.BooleanField(default=False)
    unidad_de_medida = models.ForeignKey(UnidadDeMedida, on_delete=models.PROTECT)
    estado = models.ForeignKey(Estado, on_delete=models.PROTECT)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.PROTECT)

    def clean(self):

        
        if len(self.nombre) < 4 and len(self.nombre) > 20:
            raise ValidationError(
                'El nombre del item debe tener entre 4 y 20 letras.')
        if self.precio > 10000000:
            raise ValidationError(
                'El precio es demasiado elevado, nadie va a comprar el item.')
        if self.precio < 1:
            raise ValidationError(
                'El precio es demasiado bajo, es mejor regalar el item.')
        
        if self.descripcion is not None:
            if len(self.descripcion) < 5 and len(self.descripcion) > 50:
                raise ValidationError(
                    'La descripción puede contener entre 5 y 50 caracteres.')
        
        if len(self.ubicacion) < 5 and len(self.ubicacion) > 15:
            raise ValidationError(
                'La ubicación del item debe tener entre 5 y 15 caracteres.')
        if self.stockMinimo < 0:
            raise ValidationError('El stock minimo no puede ser negativo.')
        if self.stockSeguridad < 0:
            
            raise ValidationError('El stock de seguridad no puede ser negativo.')
        if not self.cantidad.isdigit():
            raise ValidationError('Debe indicar un valor para la cantidad.')

    class Meta:

        verbose_name = 'item'
        verbose_name_plural = 'items'

    def __str__(self):
        return self.nombre


class Pedidos(models.Model):

    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.PROTECT)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT)
    
    cantidad = models.IntegerField('Cantidad', null=True)
    solicitado = models.IntegerField('Solicitado: 5' ,default =5)

    def __str__(self):
        return "Item:"+ str(self.item) + " , "+ "Sucursal:"+str(self.sucursal) + " , " + "Proveedor:"+str(self.proveedor)
    
    class Meta:

        verbose_name = 'pedido'
        verbose_name_plural = 'pedidos'




    
    
    