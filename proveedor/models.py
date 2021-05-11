from django.db import models


class Proveedor(models.Model):
    
    cuit = models.CharField('Cuit', max_length=11, blank=True, null=True)
    nombre = models.CharField('Nombre', max_length=30, blank=True, null=True)
    razon_social = models.CharField('Razón Social', max_length = 40, blank=True, null = True)
    email = models.EmailField('Correo electronico', max_length=30, blank=True, null=True)
    telefono = models.IntegerField('Telefono', blank=True, null=True)
    
    class Meta:
        verbose_name = 'proveedor'
        verbose_name_plural = 'proveedores'
        
    def __str__(self):
        return self.nombre