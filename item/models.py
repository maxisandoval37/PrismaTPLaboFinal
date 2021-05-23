from django.shortcuts import redirect
from django.db import models
from sucursal.models import Sucursal
from django.db.models.signals import post_save
from proveedor.models import Proveedor
from django.core.exceptions import ValidationError
import random
# Create your models here.


class SubCategoria(models.Model):

    
    nombre_categoria = models.ForeignKey('Categoria', on_delete=models.PROTECT)

    class opcionesSubCategoria(models.TextChoices):
        
        CARRETILLAS = 'Carretillas'
        ANDAMIOS = 'Andamios'
        ELEVADORES = 'Elevadores'
        CERAMICA = 'Cerámica'
        PIEDA_NATURAL = 'Piedra natural'
        PERFILERIA_Y_ACCESORIOS = 'Perfilería y accesorios'
        TERMOSTATOS = 'Termostatos'
        TIMBRES = 'Timbres'
        APERTURA_MOTORIZADA = 'Apertura motorizada'
        LINTERNAS = 'Linternas'
        FOCOS = 'Focos'
        PANTALLAS = 'Pantallas'
        CABLE = 'Cable'
        TERMINALES = 'Terminales'
        MAGNETOTERMICOS_Y_FUSIBLES = 'Magnetotérmicos y fusibles'
        BOMBILLAS_LED = 'Bombillas led'
        BOMBILLAS_INCANDESCENTES = 'Bombillas incandescentes'
        BOMBILLAS_BAJO_CONSUMO = 'Bombillas bajo consumo'
        HIDROLAVADORES = 'Hidrolavadores'
        ASPIRADORES = 'Aspiradores'
        COMPRESORES = 'Compresores'
        MOTORES = 'Motores'
        GENERADORES = 'Generadores'
        ALICATES_Y_TENAZAS = 'Alicates y tenazas'
        LLAVES = 'Llaves'
        DESTORNILLADORES = 'Destornilladores'
        HERRAMIENTAS_ALBANILERIA = 'Herramientas de albañilería'
        GUANTES = 'Guantes'
        PROTECCION_VISUAL = 'Protección visual'
        PROTECCION_AUDITIVA = 'Protección auditiva'
        PROTECCION_ANTICAIDAS = 'Protección anticaidas'
        CAJAS_Y_MALETAS = 'Cajas y maletas'
        CINTURONES_PORTAHERRAMIENTAS = 'Cinturones portaherramientas'
        CARROS = 'Carros'
        LAVABO_PEDESTAL = 'Lavabo pedestal'
        LAVAMANOS = 'Lavamanos'
        CISTERNAS = 'Cisternas'
        CRISTAL = 'Cristal'
        PORCELANA = 'Porcelana'
        MADERA = 'Madera'
        TERMOSTATICOS = 'Termostáticos'
        MONOBLOC = 'Monobloc'
        MONOMANDO = 'Monomando'
        MANGUERAS = 'Mangueras'
        DIFUSORES = 'Difusores'
        REGADERAS = 'Regaderas'
        MACETAS = 'Macetas'
        ESTANQUES = 'Estanques'
        FUENTES = 'Fuentes'
        CERRADURAS_PARA_PUERTAS = 'Cerraduras para puertas'
        SISTEMAS_ANTIRROBO = 'Sistemas antirrobo'
        CERRADURAS_ELECTRONICAS = 'Cerraduras electrónicas'
        INTERIOR = 'Interior'
        EXTERIOR = 'Exterior'
        RODILLOS = 'Rodillos'
        PINCELES = 'Pinceles'
        
    opciones = models.CharField(choices = opcionesSubCategoria.choices, max_length=40)  

    def __str__(self):
       return self.opciones

class Categoria(models.Model):

    
    prov_preferido = models.ForeignKey(
    Proveedor, on_delete=models.PROTECT, null=True, blank=True)

    class opcionesCategoria(models.TextChoices):
        
        UTILES_DE_CONSTRUCCION = 'Útiles de Construcción'
        REVESTIMIENTOS = 'Revestimientos'
        CONFORT_Y_DOMOTICA = 'Confort y Domótica'
        ILUMINACION = 'Iluminación'
        MATERIAL_DE_INSTALACION = 'Material de instalación'
        BOMBILLAS_Y_TUBOS = 'Bombillas y tubos'
        MAQUINARIA = 'Maquinaria'
        HERRAMIENTA_MANUAL = 'Herramienta manual'
        EQUIPO_DE_PROTECCION_INDIVIDUAL = 'Equipo de protección individual'
        ORDENACION_DE_HERRAMIENTAS = 'Ordenación de herramientas'
        APARATOS_SANITARIOS = 'Aparatos sanitarios'
        COMPLEMENTOS_DE_BANO = 'Complementos de baño'
        GRIFERIA = 'Grifería'
        RIEGO = 'Riego'
        DECORACION_JARDIN = 'Decoración de jardín'
        CERRAJERIA = 'Cerrajería'
        PINTURA = 'Pintura'
        
    opciones = models.CharField(choices= opcionesCategoria.choices, max_length=40)

    def __str__(self):
        return self.opciones

class UnidadDeMedida(models.Model):

    class opcionesUDM(models.TextChoices):
        
        TONELADA = 'TONELADA'
        KG = 'KG'
        GR = 'GR'
        MG = 'MG'
        LT = 'LT'
        ML = 'ML'
        M = 'M'
        CM = 'CM'
        MM = 'MM'

    opciones = models.CharField(choices = opcionesUDM.choices, max_length=8)
    
    def __str__(self):
        return self.opciones


class Estado(models.Model):

    class opcionesEstado(models.TextChoices):
        
        ACTIVO = 'ACTIVO' 
        INACTIVO = 'INACTIVO'
        PENDIENTE =  'PENDIENTE'
        DESCONTINUADO = 'DESCONTINUADO'
        
    opciones = models.CharField(choices = opcionesEstado.choices, max_length=13)

    def __str__(self):
        return self.opciones

class Item(models.Model):

    id = models.AutoField(primary_key=True)
    nombre = models.CharField('Nombre', max_length=50, unique=True)
    precio = models.FloatField('Precio')
    descripcion = models.CharField('Descripción', max_length=50, null=True, blank=True)
    stockminimo = models.IntegerField('Stock Minimo',  default=0)
    stockseguridad = models.IntegerField('Stock de Seguridad',  default=1)
    ubicacion = models.CharField('Ubicación', max_length=15)
    ultima_modificacion = models.DateTimeField('Ultima Modificación', blank=True, null=True)
    repo_por_lote = models.BooleanField('Reposición por Lote')
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    subcategoria = models.ForeignKey(SubCategoria, on_delete=models.PROTECT)
    cantidad = models.IntegerField("Cantidad", default=0)
    solicitud = models.BooleanField(default=False)
    reintentos = models.IntegerField(default=0)
    unidad_de_medida = models.ForeignKey(UnidadDeMedida, on_delete=models.PROTECT)
    estado = models.ForeignKey(Estado, on_delete=models.PROTECT)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.PROTECT)
    cantidad_lote = models.PositiveIntegerField('Cantidad de reposición por lote', default=0, null=True)
    

    def clean(self):

        
        if len(self.nombre) < 4 and len(self.nombre) > 50:
            raise ValidationError(
                'El nombre del item debe tener entre 4 y 50 letras.')
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
        if self.stockminimo < 0:
            raise ValidationError('El stock minimo no puede ser negativo.')
        if self.stockseguridad < 0:
            
            raise ValidationError('El stock de seguridad no puede ser negativo.')
        if self.cantidad < 0:
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
    solicitadoRandom = random.randint(20, 75)
    solicitado = models.IntegerField('Solicitado ' + str(solicitadoRandom), default=solicitadoRandom)

    def __str__(self):
        return "Item:" + str(self.item) + " , " + "Sucursal:"+str(self.sucursal) + " , " + "Proveedor:"+str(self.proveedor)

    class Meta:
        verbose_name = 'pedido'
        verbose_name_plural = 'pedidos'
    
    
    