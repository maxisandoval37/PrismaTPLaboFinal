from django.db import models
from django.core.exceptions import ValidationError
from usuario.models import Usuario

class Caja(models.Model):
    
    codigo = models.CharField('Identificador', max_length= 4, unique=True)
    saldo_disponible = models.DecimalField('Saldo Disponible', decimal_places=2, max_digits=9)
    egresos = models.DecimalField('Egresos', decimal_places=2, max_digits=9)
    ingresos = models.DecimalField('Ingresos', decimal_places=2, max_digits=9)
    saldo_inicial = models.DecimalField('Saldo Inicial', decimal_places=2, max_digits=9)
    saldo_final = models.DecimalField('Saldo Final', decimal_places=2, max_digits=9)
    sucursal_id = models.ForeignKey('Sucursal', on_delete=models.PROTECT, null=True)

    
    def clean(self):
        
        if not self.codigo.isalnum():
            raise ValidationError('El identificador solo puede contener letras y números')
        if len(self.codigo) < 2 and len(self.codigo) > 4:
            raise ValidationError('El indentificador debe tener entre 2 y 4 caracteres')
        if self.saldo_disponible < 1 and self.saldo_disponible > 9:
            raise ValidationError('El saldo disponible debe tener entre 1 y 9 digitos.')
        if self.egresos < 1 and self.egresos > 9:
            raise ValidationError('Los egresos deben tener entre 1 y 9 digitos.')
        if self.ingresos < 1 and self.ingresos > 9:
            raise ValidationError('Los ingresos deben tener entre 1 y 9 digitos.')
        if self.saldo_inicial < 1 and self.saldo_inicial > 9:
            raise ValidationError('El saldo inicial debe tener entre 1 y 9 digitos.')
        if self.saldo_final < 1 and self.saldo_final > 9:
            raise ValidationError('El saldo final debe tener entre 1 y 9 digitos.')
    
    class Meta:
        
        verbose_name = 'caja'
        verbose_name_plural = 'cajas'
    
    def __str__(self):
       return self.codigo

class Sucursal (models.Model):
    
    codigo = models.CharField(max_length = 4, unique=True)
    idCasaCentral = models.IntegerField(default= 1)
    caja_id = models.OneToOneField('Caja', on_delete=models.PROTECT, blank= True, null=True)
    
    calle = models.CharField('Calle', max_length=20)
    numero = models.CharField('Numero',  max_length=4)
    localidad = models.CharField('Localidad', max_length=20, null=True)
    provincia = models.CharField('Provincia', max_length= 20, null=True)
    cod_postal = models.CharField('Código postal', max_length=4)
    supervisor = models.ForeignKey(Usuario,  on_delete=models.PROTECT, null=True)
    
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





