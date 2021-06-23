from django.shortcuts import redirect
from django.db import models
from sucursal.models import Sucursal
from django.db.models.signals import post_save
from proveedor.models import Proveedor
from django.core.exceptions import ValidationError
from proveedor.models import CuentaCorrienteProveedor
from usuario.models import Supervisor, Usuario
import random
from datetime import datetime
from django.db.models.signals import pre_save



class SubCategoria(models.Model):

    
    nombre_categoria = models.ForeignKey('Categoria', on_delete=models.PROTECT)

    class opcionesSubCategoria(models.TextChoices):
        
        CARRETILLAS = 'Carretillas'
        ANDAMIOS = 'Andamios'
        ELEVADORES = 'Elevadores'
        CERAMICA = 'Cerámica'
        PIEDRA_NATURAL = 'Piedra natural'
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
        PILAS_RECARGABLES = 'Pilas recargables'
        PILAS_NO_RECARGABLES = 'Pilas no recargables'
        
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
        PILAS = 'Pilas'
        
    opciones = models.CharField(choices= opcionesCategoria.choices, max_length=40)

    
    def __str__(self):
        return self.opciones

class UnidadDeMedida(models.Model):

    class opcionesUDM(models.TextChoices):
        
        TONELADA = 'TONELADA'
        UNIDAD = 'UNIDAD'
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
        
    opciones = models.CharField(choices = opcionesEstado.choices, max_length=13, default= 'ACTIVO')

    def __str__(self):
        return self.opciones

def random_codigo():
        
        return int(str(datetime.now()).replace("-","").replace(" ","").replace(":","").replace(".","")[7:])

class Item(models.Model):

    id = models.AutoField(primary_key=True)
    codigo_de_barras = models.BigIntegerField('Código de barras', unique=True,  default = random_codigo)
    nombre = models.CharField('Nombre', max_length=50)
    precio = models.DecimalField('Precio',decimal_places=2, max_digits=10, null=True)
    descripcion = models.CharField('Descripción', max_length=50, null=True, blank=True)
    stockminimo = models.IntegerField('Stock Minimo',  default=1)
    stockseguridad = models.IntegerField('Stock de Seguridad',  default=0)
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

        items = Item.objects.all() 
        
        for item in items:
            
            if self.nombre.lower() == item.nombre.lower() and self.sucursal == item.sucursal and self.codigo_de_barras != item.codigo_de_barras:
                
                raise ValidationError('Ya existe un item con el mismo nombre en la sucursal '+str(self.sucursal)+".")
        
        
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
            raise ValidationError('La cantidad del stock no puede ser negativa')
        
        
        if self.repo_por_lote and self.cantidad_lote == 0:
            raise ValidationError('Es necesario ingresar una cantidad de reposición por lote.')

    class Meta:

        verbose_name = 'item'
        verbose_name_plural = 'items'

    def __str__(self):
        return self.nombre
    
    
    
class Pintura(Item):
    
    color = models.CharField('Color', max_length=30)
    cantidad_pintura = models.PositiveIntegerField('Cantidad de pintura', default= 0)
    
    class Meta:

        verbose_name = 'pintura'
        verbose_name_plural = 'pinturas'

    def __str__(self):
        return "{}, Color:{}, Sucursal: {}".format(self.nombre, self.color, self.sucursal)
    
    def clean(self):
        
        pinturas = Pintura.objects.all()
        for pintura in pinturas:
        
            if self.nombre.lower() == pintura.nombre.lower() and self.color.lower() == pintura.color.lower() and self.id != pintura.id:
                raise ValidationError('La pintura ya está registrada.')
        
        if not self.color.isalpha():
            raise ValidationError('El color solo puede tener letras.')
        if len(self.color) > 30 or len(self.color) < 4:
            raise ValidationError('El color debe tener entre 4 y 30 letras.')
        
        if self.cantidad_pintura <= 0:
            raise ValidationError('La cantidad de la pintura debe ser mayor a 0.')
    
    
class PinturaUsada(models.Model):
    
    codigo_de_barras = models.BigIntegerField('Código de barras', default = random_codigo, unique=True)
    nombre = models.CharField('Nombre de pintura', max_length=30)
    color = models.CharField('Color de pintura', max_length=50)
    cantidad_restante = models.PositiveIntegerField('Cantidad de pintura restante')
    precio = models.PositiveIntegerField('Precio')
    sucursal = models.ForeignKey(Sucursal, on_delete=models.PROTECT)
    
    class Meta:
        
        verbose_name = 'pintura usada'
        verbose_name_plural = 'pinturas usadas'
        
    def __str__(self):
        return "Pintura: {}, Color: {}".format(self.nombre, self.color) 
    
    def clean(self):
        
        if len(self.nombre) < 4 and len(self.nombre) > 30:
            raise ValidationError(
                'El nombre del item debe tener entre 4 y 30 letras.')
        
        if not self.color.isalpha():
            raise ValidationError('El color solo puede tener letras.')
        if len(self.color) > 50 or len(self.color) < 4:
            raise ValidationError('El color debe tener entre 4 y 50 letras.')  
        if self.cantidad_restante < 0:
            raise ValidationError('La cantidad restante de la pintura no puede ser negativa.')

class PinturaNueva(models.Model):
    
    codigo_de_barras = models.BigIntegerField('Código de barras', default = random_codigo, unique=True)
    nombre = models.CharField('Nombre de pintura', max_length=30)
    color = models.CharField('Color de pintura', max_length=50)
    cantidad = models.PositiveIntegerField('Cantidad de pintura (ML)')
    stock = models.IntegerField('Stock')
    pcant = models.PositiveIntegerField('Primera cantidad')
    scant = models.PositiveIntegerField('Segunda cantidad')
    precio = models.PositiveIntegerField('Precio')
    sucursal = models.ForeignKey(Sucursal, on_delete=models.PROTECT)
    
    class Meta:
        
        verbose_name = 'pintura nueva'
        verbose_name_plural = 'pinturas nuevas'
        
    def __str__(self):
        return "Pintura: {}, Color: {}".format(self.nombre, self.color) 
    
    def clean(self):
        
        if len(self.nombre) < 4 and len(self.nombre) > 30:
            raise ValidationError(
                'El nombre del item debe tener entre 4 y 30 letras.')
        
        if not self.color.isalpha():
            raise ValidationError('El color solo puede tener letras.')
        if len(self.color) > 50 or len(self.color) < 4:
            raise ValidationError('El color debe tener entre 4 y 50 letras.')  
        if self.cantidad_restante < 0:
            raise ValidationError('La cantidad restante de la pintura no puede ser negativa.')
    

class Mezcla(models.Model):
    
    primera_pintura = models.ForeignKey(Pintura, on_delete=models.PROTECT, related_name='+')
    segunda_pintura = models.ForeignKey(Pintura,on_delete=models.PROTECT)
    cantidad_primera_pintura = models.IntegerField('Cantidad de la primera pintura (En mililitros)')
    cantidad_segunda_pintura = models.IntegerField('Cantidad de la segunda pintura (En mililitros)')
    
    
    class Meta:
       verbose_name = 'mezcla'
       verbose_name_plural = 'mezclas'

    def __str__(self):
        return "Pintura: {} con {}".format(self.primera_pintura.color, self.segunda_pintura.color) 
    
    def clean(self):
        
        if self.primera_pintura.color == self.segunda_pintura.color:
            raise ValidationError("No puedes mezclar dos pinturas del mismo color.")
        
        if self.primera_pintura.sucursal != self.segunda_pintura.sucursal:
            raise ValidationError('Las pinturas deben pertenecer a la misma sucursal.')
        
        if self.primera_pintura == None:
            raise ValidationError('Debe seleccionar la primera pintura a mezclar.')
        
        if self.segunda_pintura == None:
            raise ValidationError('Debe seleccionar la segunda pintura a mezclar.')
        
        if self.primera_pintura == self.segunda_pintura:
            raise ValidationError('No es posible mezclar dos pinturas iguales.')
        
        if self.primera_pintura.cantidad <= 0 or self.segunda_pintura.cantidad <= 0:
            raise ValidationError('La pintura seleccionada no tiene stock disponible.')
        
        if self.cantidad_primera_pintura > self.primera_pintura.cantidad_pintura:
            raise ValidationError('No puedes ingresar una cantidad mayor que la capacidad maxima de la primera pintura.') 
        if self.cantidad_segunda_pintura > self.segunda_pintura.cantidad_pintura:
            raise ValidationError('No puedes ingresar una cantidad mayor que la capacidad maxima de la segunda pintura.')
        
        if self.cantidad_primera_pintura < 0 or self.cantidad_primera_pintura == 0:
            raise ValidationError('La cantidad de la primera pintura debe ser mayor que 0.')
        if self.cantidad_segunda_pintura < 0 or self.cantidad_segunda_pintura == 0:
            raise ValidationError('La cantidad de la segunda pintura debe ser mayor que 0.')

class MezclaUsada(models.Model):
    
    primera_pintura = models.ForeignKey(PinturaUsada, on_delete=models.PROTECT, related_name='+')
    segunda_pintura = models.ForeignKey(PinturaUsada,on_delete=models.PROTECT)
    cantidad_primera_pintura = models.PositiveIntegerField('Cantidad de la primera pintura (En mililitros)', default = 0)
    cantidad_segunda_pintura = models.PositiveIntegerField('Cantidad de la segunda pintura (En mililitros)', default = 0)
    
    
    class Meta:
       verbose_name = 'mezcla'
       verbose_name_plural = 'mezclas'

    def __str__(self):
        return "Pintura: {} con {}".format(self.primera_pintura.color, self.segunda_pintura.color) 
    
    def clean(self):
        
        if self.primera_pintura == None:
            raise ValidationError('Debe seleccionar la primera pintura a mezclar.')
        
        if self.segunda_pintura == None:
            raise ValidationError('Debe seleccionar la segunda pintura a mezclar.')
        
        if self.primera_pintura == self.segunda_pintura:
            raise ValidationError('No es posible mezclar dos pinturas iguales.')
        
        if self.cantidad_primera_pintura > self.primera_pintura.cantidad_restante:
            raise ValidationError('No puedes ingresar una cantidad mayor que la cantidad restante de la primera pintura.') 
        if self.cantidad_segunda_pintura > self.segunda_pintura.cantidad_restante:
            raise ValidationError('No puedes ingresar una cantidad mayor que la cantidad restante de la segunda pintura.')
        
        if self.cantidad_primera_pintura < 0 or self.cantidad_primera_pintura == 0:
            raise ValidationError('La cantidad de la primera pintura debe ser mayor que 0.')
        if self.cantidad_segunda_pintura < 0 or self.cantidad_segunda_pintura == 0:
            raise ValidationError('La cantidad de la segunda pintura debe ser mayor que 0.')
    

class Pedidos(models.Model):
    
    fecha = models.DateTimeField('Fecha de creación', auto_now_add=True)
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.PROTECT)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT)
    cuenta_corriente = models.ForeignKey(CuentaCorrienteProveedor, on_delete= models.PROTECT)
    cantidad = models.IntegerField('Cantidad', null=True)
    solicitadoRandom = random.randint(20, 75)
    solicitado = models.IntegerField('Solicitado ', default=solicitadoRandom)
    total = models.DecimalField('Total', decimal_places=2, max_digits=7, default = 0)
    estado = models.BooleanField('Estado del pedido', default= True)
    
    def __str__(self):
        return "Item:" + str(self.item) + " , " + "Sucursal:"+str(self.sucursal) + " , " + "Proveedor:"+str(self.proveedor)

    class Meta:
        verbose_name = 'pedido'
        verbose_name_plural = 'pedidos'
    
    
class ReportePrecios(models.Model):

    categoria_asociada = models.ForeignKey(Categoria, on_delete= models.PROTECT)
    fecha = models.DateTimeField('Fecha de modificación', auto_now_add=True)
    aumento = models.DecimalField('Aumento', decimal_places= 2, max_digits=7)
    responsable = models.ForeignKey(Supervisor, on_delete=models.PROTECT)
    responsable_usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT,related_name= 'responsable_usuario')
    
    class Meta:
        verbose_name = 'reporte de precios'
        verbose_name_plural = 'reportes de precios'
        
    def __str__(self):
        return "Fecha: {} , Categoria: {}".format(self.fecha, self.categoria_asociada)
    

class ReportePreciosItems(models.Model):
    
    fecha = models.DateTimeField('Fecha de modificación', auto_now_add=True)
    aumento = models.DecimalField('Aumento', decimal_places= 2, max_digits=7)
    responsable = models.ForeignKey(Supervisor, on_delete=models.PROTECT)
    
    class Meta:
        verbose_name = 'reporte de precios global'
        verbose_name_plural = 'reportes de precios globales'
        
    def __str__(self):
        return "Fecha: {} , Aumento: {}".format(self.fecha, self.aumento)
    
    
class HistorialPref(models.Model):
    
    fecha = models.DateTimeField('Fecha de asignación', auto_now_add=True)
    proveedor_asociado = models.ForeignKey(Proveedor, on_delete=models.PROTECT)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    
    class Meta:
        verbose_name = 'historial de preferenciados'
        verbose_name_plural = 'historiales de preferenciados'
        
    def __str__(self):
        return "Fecha: {} , Proveedor: {}, Categoria: {}".format(self.fecha, self.proveedor_asociado, self.categoria)
    
    
def defaultActivoItem(sender, instance, **kwargs):
    
    
    estados = Estado.objects.all()
    if len(estados) > 0:
        print("hola xxddx")
        if instance.estado_id == None:
            print("joder llege")
            estadosQuery = Estado.objects.filter(opciones = 'ACTIVO')
            activo = ""
            for estado in estadosQuery:
                activo = estado.id 
            
            instance.estado_id = activo 
           
            
pre_save.connect(defaultActivoItem, sender = Item)

def defaultActivoPintura(sender, instance, **kwargs):
    
    
    estados = Estado.objects.all()
    if len(estados) > 0:
        print("hola xxddx")
        if instance.estado_id == None:
            print("joder llege")
            estadosQuery = Estado.objects.filter(opciones = 'ACTIVO')
            activo = ""
            for estado in estadosQuery:
                activo = estado.id 
            
            instance.estado_id = activo 
           
            
pre_save.connect(defaultActivoPintura, sender = Pintura)
    
