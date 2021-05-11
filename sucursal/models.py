from django.db import models

class Sucursal (models.Model):
    
    nombre = models.CharField(max_length = 100)
    direccion = models.CharField(max_length = 50,null = True)
    idCasaCentral = models.IntegerField(default= 1)
    
    
    
    class Meta:
        
        verbose_name = 'sucursal'
        verbose_name_plural = 'sucursales'

    def __str__(self):
        return self.nombre



