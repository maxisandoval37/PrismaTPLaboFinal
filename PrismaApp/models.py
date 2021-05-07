from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType

class Rol(models.Model):
    
    id = models.AutoField(primary_key=True)
    rol = models.CharField('Rol',max_length=30, unique=True)
    

    class Meta:
        
        verbose_name = 'rol'
        verbose_name_plural = 'roles'
        
    def __str__(self):
        return self.rol
    
    def save(self, *args, **kwargs):
        #permsisos_defecto = ['add']
        if not self.id :
            #nuevo_grupo = Group.objects.get_or_create(name = f'{self.rol}')
            print("hola")
        super().save(*args, **kwargs) 

class UsuarioManager(BaseUserManager):
    def _create_user(self,cuit, username,email,password,usuario_staff, superusuario, **extra_fields):
        if not cuit:
            raise ValueError('El usuario debe tener un número de cuit!')

        usuario = self.model(
            username = username,
            cuit=cuit,
            email = self.normalize_email(email),
            usuario_staff = usuario_staff,
            superusuario = superusuario,
            **extra_fields
            )
        
        usuario.set_password(password)
        usuario.save()
        return usuario
    
    def create_user(self, username, cuit, email, password = None, **extra_fields):
        return self._create_user(cuit,username, email, password, False, False, **extra_fields)
    
    def create_superuser(self,username,cuit,email,password= None, **extra_fields):
        return self._create_user(cuit,username, email, password, True, True, **extra_fields)
    

class Usuario(AbstractBaseUser, PermissionsMixin):
    
    username = models.CharField('Nombre de usuario', unique=True, max_length=60)
    cuit = models.CharField('Cuit' ,primary_key=True, unique=True, max_length=40)
    rol = models.ForeignKey('Rol', on_delete=models.CASCADE, blank=True, null=True)
    nombre = models.CharField('Nombre',max_length=30, blank=True, null=True)
    apellido = models.CharField('Apellido', max_length=30, blank=True, null=True)
    email = models.EmailField('Email',max_length=60, unique=True)
    telefono = models.IntegerField('Telefono', blank=True, null=True)
    usuario_staff = models.BooleanField(default=False)
    superusuario = models.BooleanField(default=False)
    
    objects = UsuarioManager()
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'cuit']
    
    def __str__(self):
        return f'Usuario {self.username}'
    
    def has_perm(self, perm, obj= None):
        
        return True
    
    def has_module_perms(self, app_label):
        
        return True
    
    @property
    def is_staff(self):
        return self.usuario_staff
    
    @property
    def is_superuser(self):
        return self.superusuario
    
    
   
    










#class Usuario(models.Model):
    
    
  #  cuit = models.AutoField(primary_key=True)
  #  rol = models.CharField(max_length=20)
  #  nombre = models.CharField(max_length=30)
  #  apellido = models.CharField(max_length=30)
  #  email = models.EmailField(max_length=60)
   # telefono = models.IntegerField()
    
    
   # class Meta:
   #     verbose_name = 'usuario'
 #       verbose_name_plural = 'usuarios'
        
    