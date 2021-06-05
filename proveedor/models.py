from django.db import models
from django.core.exceptions import ValidationError

class CuentaCorrienteProveedor(models.Model):
    
    numero_cuenta = models.BigIntegerField("Número de cuenta")
    proveedor = models.ForeignKey('Proveedor', on_delete=models.PROTECT)
    
    def __str__(self):
        return "Proveedor: {}, Cuenta: {}".format(self.proveedor.razon_social, self.numero_cuenta)

    def clean(self):
        
        cuentas_corriente = CuentaCorrienteProveedor.objects.all()
        cuenta_corriente = CuentaCorrienteProveedor.objects.filter(proveedor = self.proveedor)
        contador = 0
        
        for cuenta in cuenta_corriente:
            contador += 1
            
        for cuenta in cuentas_corriente:
            
            if self.numero_cuenta == cuenta.numero_cuenta:
                raise ValidationError('La cuenta corriente ya está registrada.')

class Proveedor(models.Model):
    
    cuit = models.CharField('Cuit', unique=True, max_length=11)
    razon_social = models.CharField('Razón Social', max_length = 20, unique=True)
    email = models.EmailField('Correo electronico', max_length=30, unique=True)
    telefono = models.CharField('Telefono', null=True, max_length=13, unique=True)
    calle = models.CharField('Calle', max_length=20, blank = True,null=True)
    numero = models.CharField('Numero',blank = True,null=True, max_length=4)
    localidad = models.CharField('Localidad', max_length=20,blank = True,null=True)
    provincia = models.CharField('Provincia', max_length= 20,blank = True,null=True)
    cod_postal = models.CharField('Código postal', blank = True,null=True, max_length= 4)
    
   
    def clean(self):
        
        if not self.cuit.isdigit():
            raise ValidationError('Cuit inválido.')
        
        if len(self.cuit) != 11:
            raise ValidationError('El Cuit debe tener exactamente 11 digitos.')
                   
        if len(self.razon_social) < 4 and len(self.razon_social) > 20:
            raise ValidationError('La razón social debe tener entre 4 y 20 caracteres.')         
        
        if not self.telefono.isdigit():
            raise ValidationError('El telefono solo puede contener digitos')
        
                
        if len(self.telefono) < 3 and len(self.telefono) > 13:
            raise ValidationError('El telefono debe tener entre 3 y 13 digitos.')
    
        if self.calle is not None:
            if len(self.calle) < 4 and len(self.calle) > 20:
                raise ValidationError('La calle debe tener entre 4 y 20 letras')
        
        if self.numero is not None:
            if not self.numero.isdigit():
                raise ValidationError('El número solo puede contener digitos.') 
            
            if len(self.numero) < 2 and len(self.numero) > 4:
                raise ValidationError('El número debe tener entre 1 y 4 digitos.')
        
        if self.localidad is not None:
            if len(self.localidad) < 4 and len(self.localidad) > 20:
                raise ValidationError('La calle debe tener entre 4 y 20 letras')
         
        if self.provincia is not None:       
            if len(self.provincia) < 4 and len(self.provincia) > 20:
                raise ValidationError('La provincia debe tener entre 4 y 20 letras')
    
        if self.cod_postal is not None:
            if not self.cod_postal.isdigit():
                raise ValidationError('El código postal solo puede contener digitos.')
            
            if len(self.cod_postal) < 1 and len(self.cod_postal) > 4:
                raise ValidationError('El código postal debe tener entre 1 y 4 digitos.')
        
        
    class Meta:
        verbose_name = 'proveedor'
        verbose_name_plural = 'proveedores'
        
    def __str__(self):
        return self.razon_social
    
