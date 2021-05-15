from django.db import models

class Caja(models.Model):
    
    codigo = models.CharField('Identificador', max_length= 5, unique=True, null=True)
    saldo_disponible = models.DecimalField('Saldo Disponible', decimal_places=2, max_digits=9)
    egresos = models.DecimalField('Egresos', decimal_places=2, max_digits=9)
    ingresos = models.DecimalField('Ingresos', decimal_places=2, max_digits=9)
    saldo_inicial = models.DecimalField('Saldo Inicial', decimal_places=2, max_digits=9)
    saldo_final = models.DecimalField('Saldo Final', decimal_places=2, max_digits=9)

    class Meta:
        
        verbose_name = 'caja'
        verbose_name_plural = 'cajas'
    
    def __str__(self):
       return self.codigo

class Sucursal (models.Model):
    
    codigo = models.CharField(max_length = 4, unique=True)
    idCasaCentral = models.IntegerField(default= 1)
    caja = models.ForeignKey(Caja, on_delete=models.PROTECT, null = True)
    
    calle = models.CharField('Calle', max_length=20, null=True)
    numero = models.IntegerField('Numero', null=True)
    localidad = models.CharField('Localidad', max_length=20, null=True)
    provincia = models.CharField('Provincia', max_length= 20, null=True)
    cod_postal = models.IntegerField('Código postal', null=True)
    
    
    class Meta:
        
        verbose_name = 'sucursal'
        verbose_name_plural = 'sucursales'

    def __str__(self):
        return self.codigo





