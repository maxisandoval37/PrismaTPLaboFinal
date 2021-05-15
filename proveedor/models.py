from django.db import models



class Proveedor(models.Model):
    
    cuit = models.CharField('Cuit', unique=True, max_length=11)
    razon_social = models.CharField('Razón Social', max_length = 20, unique=True)
    email = models.EmailField('Correo electronico', max_length=30, unique=True)
    telefono = models.CharField('Telefono', null=True, max_length=13)
    calle = models.CharField('Calle', max_length=4, blank = True,null=True)
    numero = models.CharField('Numero',blank = True,null=True, max_length=4)
    localidad = models.CharField('Localidad', max_length=20,blank = True,null=True)
    provincia = models.CharField('Provincia', max_length= 20,blank = True,null=True)
    cod_postal = models.CharField('Código postal', blank = True,null=True, max_length= 4)
   
    
    class Meta:
        verbose_name = 'proveedor'
        verbose_name_plural = 'proveedores'
        
    def __str__(self):
        return self.razon_social
    
    
