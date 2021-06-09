from django.db import models
from django.core.exceptions import ValidationError




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
        
        if not self.codigo.isalnum():
            raise ValidationError('El identificador solo puede contener letras y números.')
        if len(self.codigo) < 2 and len(self.codigo) > 4:
            raise ValidationError('El indentificador debe tener entre 2 y 4 caracteres.')
        if self.saldo_disponible < 1 and self.saldo_disponible > 9 or self.saldo_disponible_dolares < 1 and self.saldo_disponible_dolares > 9 or self.saldo_disponible_euros < 1 and self.saldo_disponible_euros > 9:
            raise ValidationError('El saldo disponible debe tener entre 1 y 9 digitos.')
        if self.egresos < 1 and self.egresos > 9:
            raise ValidationError('Los egresos deben tener entre 1 y 9 digitos.')
        if self.ingresos_en_pesos < 1 and self.ingresos_en_pesos > 9 or self.ingresos_en_dolares < 1 and self.ingresos_en_dolares > 9 or self.ingresos_en_euros < 1 and self.ingresos_en_euros > 9:
            raise ValidationError('Los ingresos deben tener entre 1 y 9 digitos.')
        if self.saldo_inicial < 1 and self.saldo_inicial > 9:
            raise ValidationError('El saldo inicial debe tener entre 1 y 9 digitos.')
        if self.saldo_final < 1 and self.saldo_final > 9:
            raise ValidationError('El saldo final debe tener entre 1 y 9 digitos.')
        
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
   


class Sucursal (models.Model):
    
    codigo = models.CharField(max_length = 4, unique=True)
    idCasaCentral = models.IntegerField(default= 1)
    calle = models.CharField('Calle', max_length=20)
    numero = models.CharField('Numero',  max_length=4)
    localidad = models.CharField('Localidad', max_length=20, null=True)
    provincia = models.CharField('Provincia', max_length= 20, null=True)
    cod_postal = models.CharField('Código postal', max_length=4)
   
    
    def clean(self):
        if not self.codigo.isalnum():
            raise ValidationError('El código de la sucursal solo puede contener letras y números')
        if len(self.codigo) < 2 and len(self.codigo) > 4:
            raise ValidationError('El código de la sucursal debe tener entre 2 y 4 caracteres')
        
        if len(self.calle) < 4 and len(self.calle) > 20:
            raise ValidationError('La calle debe tener entre 4 y 20 letras')
        
        if not self.numero.isdigit():
            raise ValidationError('El número solo puede contener digitos.') 
         
        if len(self.numero) < 2 and len(self.numero) > 4:
            raise ValidationError('El número debe tener entre 1 y 4 digitos.')
        
        if len(self.localidad) < 4 and len(self.localidad) > 20:
            raise ValidationError('La calle debe tener entre 4 y 20 letras')
            
        if len(self.provincia) < 4 and len(self.provincia) > 20:
            raise ValidationError('La provincia debe tener entre 4 y 20 letras')
        
        if not self.cod_postal.isdigit():
            raise ValidationError('El código postal solo puede contener digitos.')
        
        if len(self.cod_postal) < 1 and len(self.cod_postal) > 4:
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
    
    class Meta:
        
        verbose_name = 'operacion'
        verbose_name_plural = 'operaciones'
    
    def __str__(self):
        return "Identificador: {}, Monto: {}, Tipo: {}".format(self.identificador, self.monto, self.tipo)
        
        
        
