from django.db import models

class Sucursal (models.Model):
    id = models.AutoField(primary_key = True)
    nombre = models.CharField(max_length = 100)
    direccion = models.CharField(max_length = 50,null = True)
    


class Caja (models.Model):
    id = models.AutoField(primary_key = True)

   
class Empleado (models.Model):
    id = models.AutoField(primary_key= True)
    cuit = models.CharField(max_length=30)
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=20)
    email = models.EmailField(max_length=30)
    telefono = models.CharField(max_length=12)
    username = models.CharField(max_length=10)
    contraseña = models.CharField(max_length=20)
    



def __str__(self):
    return self.nombre
