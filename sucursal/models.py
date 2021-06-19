from django.db import models
from django.core.exceptions import ValidationError
from django.db.models.enums import TextChoices
from django.db.models.signals import post_save



class Caja(models.Model):
    
    codigo = models.CharField('Identificador', max_length= 4, unique=True)
    saldo_disponible = models.DecimalField('Saldo disponible en pesos', decimal_places=2, max_digits=9)
    saldo_disponible_dolares = models.DecimalField('Saldo disponible en dolares', decimal_places=2, max_digits=9)
    saldo_disponible_euros = models.DecimalField('Saldo disponible en euros', decimal_places=2, max_digits=9)
    egresos = models.DecimalField('Egresos', decimal_places=2, max_digits=9)
    ingresos_en_pesos = models.DecimalField('Ingresos en pesos', decimal_places=2, max_digits=9)
    ingresos_en_dolares = models.DecimalField('Ingresos en dolares', decimal_places=2, max_digits=9)
    ingresos_en_euros = models.DecimalField('Ingresos en euros', decimal_places=2, max_digits=9)
    saldo_inicial = models.DecimalField('Saldo Inicial', decimal_places=2, max_digits=9)
    saldo_final = models.DecimalField('Saldo Final', decimal_places=2, max_digits=9)
    sucursal_id = models.ForeignKey('Sucursal', on_delete=models.PROTECT, null=True)

    
    def clean(self):
        
        cajas = Caja.objects.all() 
        
        for caja in cajas:
            if self.codigo == caja.codigo and self.id != caja.id:
                raise ValidationError('Ya existe una caja con el identificador ingresado.')
        
        if not self.codigo.isalnum():
            raise ValidationError('El identificador solo puede contener letras y números.')
        if len(self.codigo) < 2 or len(self.codigo) > 4:
            raise ValidationError('El indentificador debe tener entre 2 y 4 caracteres.')
        if self.saldo_disponible < 0:
            raise ValidationError('El saldo disponible en pesos no puede ser negativo.')
        if self.saldo_disponible_dolares < 0:
            raise ValidationError('El saldo disponible en dolares no puede ser negativo.')
        if self.saldo_disponible_euros < 0:
            raise ValidationError('El saldo disponible en euros no puede ser negativo.')
        if self.egresos < 0 :
            raise ValidationError('Los egresos no pueden ser negativos.')
        if self.ingresos_en_pesos < 0:
            raise ValidationError('Los ingresos en pesos no pueden ser negativos.')
        if self.ingresos_en_dolares < 0:
            raise ValidationError('Los ingresos en dolares no pueden ser negativos.')
        if self.ingresos_en_euros < 0:
            raise ValidationError('Los ingresos en euros no pueden ser negativos.')
        if self.saldo_inicial < 0 :
            raise ValidationError('El saldo inicial no puede ser negativo.')
        if self.saldo_final < 0:
            raise ValidationError('El saldo final no puede ser negativo.')
        
        if self.saldo_disponible < 0 or self.saldo_disponible_dolares < 0 or self.saldo_disponible_euros < 0:
            raise ValidationError('El saldo disponible no puede ser negativo.')
        if self.ingresos_en_pesos < 0 or self.ingresos_en_dolares < 0 or self.ingresos_en_euros < 0:
            raise ValidationError('Los ingresos no pueden ser negativos.')
        
        if self.egresos < 0:
            raise ValidationError('Los egresos no pueden ser negativos.')
        if self.saldo_inicial < 0:
            raise ValidationError('El saldo inicial no puede ser negativo.')
        if self.saldo_final < 0:
            raise ValidationError('El saldo final no puede ser negativo.')
    
    class Meta:
        
        verbose_name = 'caja'
        verbose_name_plural = 'cajas'
    
    def __str__(self):
       return self.codigo
   
class EstadoSucursal(models.Model):
    
    class opcionesEstado(TextChoices):
        
        ACTIVA = 'ACTIVA'
        INACTIVA = 'INACTIVA'
        
    opciones = models.CharField(choices = opcionesEstado.choices, max_length=8, default= 'ACTIVA')

    def __str__(self):
        return self.opciones


class Sucursal (models.Model):
    
    codigo = models.CharField(max_length = 4, unique=True)
    idCasaCentral = models.IntegerField(default= 1)
    estado = models.ForeignKey(EstadoSucursal, on_delete=models.PROTECT, null=True)
    calle = models.CharField('Calle', max_length=20)
    numero = models.CharField('Numero',  max_length=4)
    localidad = models.CharField('Localidad', max_length=20, null=True)
    provincia = models.CharField('Provincia', max_length= 20, null=True)
    cod_postal = models.CharField('Código postal', max_length=4)
   
    
    def clean(self):
        

        for char in self.localidad:
            
            if not char.isalpha() and char != " ":
                raise ValidationError('La localidad solo puede tener letras y espacios.')
            
        for char in self.provincia:
            
            if not char.isalpha() and char != " ":
                raise ValidationError('La provincia solo puede tener letras y espacios.')
           
        for char in self.cod_postal:
            
            if char.isalpha():
                raise ValidationError("El código postal solo puede tener digitos.")
        
        if not self.codigo.isalnum():
            raise ValidationError('El código de la sucursal solo puede contener letras y números')
        if len(self.codigo) < 2 or len(self.codigo) > 4:
            raise ValidationError('El código de la sucursal debe tener entre 2 y 4 caracteres')
        
        if len(self.calle) < 4 or len(self.calle) > 20:
            raise ValidationError('La calle debe tener entre 4 y 20 letras')
        
        if not self.numero.isdigit():
            raise ValidationError('El número solo puede contener digitos.') 
         
        if len(self.numero) < 2 or len(self.numero) > 4:
            raise ValidationError('El número debe tener entre 1 y 4 digitos.')
        
        
        if len(self.localidad) < 4 or len(self.localidad)  > 20:
            raise ValidationError('La calle debe tener entre 4 y 20 letras')
            
        if len(self.provincia) < 4 or len(self.provincia)> 20:
            raise ValidationError('La provincia debe tener entre 4 y 20 letras')
        
        if not self.cod_postal.isdigit():
            raise ValidationError('El código postal solo puede contener digitos.')
        
        if len(self.cod_postal) < 1 or len(self.cod_postal) > 4:
            raise ValidationError('El código postal debe tener entre 1 y 4 digitos.')
    
    class Meta:
        
        verbose_name = 'sucursal'
        verbose_name_plural = 'sucursales'

    def __str__(self):
        return self.codigo


class Operacion(models.Model):
    
    fecha = models.DateTimeField('Fecha', auto_now_add=True)
    monto = models.CharField('Monto', max_length=40)
    tipo = models.CharField('Tipo', max_length=10)
    caja_asociada = models.ForeignKey(Caja, on_delete=models.PROTECT)
    identificador = models.CharField('Identificador', max_length= 30)
    responsable = models.IntegerField('ID de responsable')
    
    class Meta:
        
        verbose_name = 'operacion'
        verbose_name_plural = 'operaciones'
    
    def __str__(self):
        return "Identificador: {}, Monto: {}, Tipo: {}".format(self.identificador, self.monto, self.tipo)
        
        
        
def defaultActivo(sender, instance, **kwargs):
    
    
    
    if instance.estado  == None:
        
        estadosQuery = EstadoSucursal.objects.filter(opciones = 'ACTIVA')
        activo = ""
        for estado in estadosQuery:
            activo = estado.id 
        
        instance.estado_id = activo 
        instance.save()
        
post_save.connect(defaultActivo, sender = Sucursal)