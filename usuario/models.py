from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin       
from django.contrib.auth.models import Permission,Group
from django.contrib.contenttypes.models import ContentType     
from django.core.exceptions import ValidationError
from sucursal.models import Sucursal
import re
from django.db.models.signals import pre_save


class Rol(models.Model):
    
    id = models.AutoField(primary_key = True)
    
    class opcionesRol(models.TextChoices):
        
        SUPERVISOR = 'SUPERVISOR'
        GERENTE_GENERAL = 'GERENTE GENERAL'
        VENDEDOR = 'VENDEDOR'
        ADMINISTRATIVO = 'ADMINISTRATIVO'
        CAJERO = 'CAJERO'
        
    opciones = models.CharField(choices = opcionesRol.choices, max_length=15)
    
    def __str__(self):
        return self.opciones
    
    
    def save(self,*args,**kwargs):
        permisos_defecto = ['add','change','delete','view']
        if not self.id:
            nuevo_grupo,creado = Group.objects.get_or_create(name = f'{self.opciones}')
            for permiso_temp in permisos_defecto:
                permiso,created = Permission.objects.update_or_create(
                    name = f'Can {permiso_temp} {self.opciones}',
                    content_type = ContentType.objects.get_for_model(Rol),
                    codename = f'{permiso_temp}_{self.opciones}'
                )
                if creado:
                    nuevo_grupo.permissions.add(permiso.id)
            super().save(*args,**kwargs)
        else:
            rol_antiguo = Rol.objects.filter(id = self.id).values('opciones').first()        # pylint: disable=maybe-no-member
            if rol_antiguo['opciones'] == self.opciones:
                super().save(*args,**kwargs)
            else:
                Group.objects.filter(name = rol_antiguo['opciones']).update(name = f'{self.opciones}')
                for permiso_temp in permisos_defecto:
                    Permission.objects.filter(codename = f"{permiso_temp}_{rol_antiguo['opciones']}").update(
                        codename = f'{permiso_temp}_{self.opciones}',
                        name = f'Can {permiso_temp} {self.opciones}'
                    )
                super().save(*args,**kwargs)
   
   
        
class EstadoUsuario(models.Model):
    
    class opcionesEstado(models.TextChoices):
        
        ACTIVO = 'ACTIVO'
        INACTIVO = 'INACTIVO'
    
    opciones = models.CharField(choices = opcionesEstado.choices, max_length=8, default= 'ACTIVO')

    def __str__(self):
        return self.opciones


class UsuarioManager(BaseUserManager):
    def _create_user(self,email,cuit,nombre,apellido,telefono,username,password,is_staff,is_superuser,**extra_fields):
        
        if not username:
            raise ValueError('Debes ingresar un nombre de usuario')
        
        user = self.model(
            email = email,
            cuit = cuit,
            nombre = nombre,
            apellido = apellido,
            telefono = telefono,
            username = username,
            is_staff = is_staff,
            is_superuser = is_superuser,
           
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self,email,cuit,nombre,apellido,telefono,username,password = None,**extra_fields):
        return self._create_user(email,cuit,nombre,apellido,telefono,username,password,False,False,**extra_fields)
    
    def create_superuser(self,email,cuit,nombre,apellido,telefono,username,password = None,**extra_fields):
        return self._create_user(email, cuit,nombre,apellido,telefono,username, password, True, True, **extra_fields)

class Usuario(AbstractBaseUser, PermissionsMixin):
    username = models.CharField('Nombre de usuario',unique = True, max_length=20)
    email = models.EmailField('Correo Electrónico', max_length=30,unique = True)
    cuit = models.CharField('Cuit',unique=True, max_length=11)
    nombre = models.CharField('Nombre', max_length=16, null = True)
    apellido = models.CharField('Apellido', max_length=16, null = True)
    rol = models.ForeignKey(Rol, on_delete=models.PROTECT, null=True)
    telefono = models.CharField('Telefono', null = True, max_length=13)
    estado = models.ForeignKey(EstadoUsuario, on_delete=models.PROTECT ,null=True)
    
    calle = models.CharField('Calle', max_length=20, blank = True,null=True)
    numero = models.CharField('Numero',blank = True,null=True, max_length=4)
    localidad = models.CharField('Localidad', max_length=20,blank = True,null=True)
    provincia = models.CharField('Provincia', max_length= 20,blank = True,null=True)
    cod_postal = models.CharField('Código postal', blank = True,null=True, max_length=4)
    
    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default = False)
    objects = UsuarioManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','cuit','telefono','nombre','apellido']

    
    def clean(self):
        
        patron = '^[^ ][a-zA-Z ]+$'
        
        
        if not self.username.isalnum():
            raise ValidationError('El nombre de usuario solo puede contener letras y números, sin espacios.')
        if len(self.username) < 6 and len(self.username) > 20:
            raise ValidationError('El nombre de usuario debe tener entre 6 y 20 caracteres.')
        
        if not self.cuit.isdigit():
            raise ValidationError('Cuit inválido.')
        
        if len(self.cuit) != 11:
            raise ValidationError('El Cuit debe tener exactamente 11 digitos.')
    
        if not (bool(re.search(patron,self.nombre))):
            raise ValidationError('El/los nombre solo puede contener letras.')
        
        if not (bool(re.search(patron,self.apellido))):
            raise ValidationError('El/los apellido solo puede contener letras.')
        
        if len(self.nombre) < 3 and len(self.nombre) > 16:
            raise ValidationError('El nombre debe tener entre 3 y 16 letras.')
        
        if len(self.apellido) < 3 and len(self.apellido) > 16:
            raise ValidationError('El apellido debe tener entre 3 y 16 letras.') 
        
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
            
        
            
            
    def __str__(self):
        return f'{self.nombre}'


    def save(self,*args,**kwargs):
        if not self.id:             # pylint: disable=maybe-no-member
            super().save(*args,**kwargs)
            if self.rol is not None:
                grupo = Group.objects.filter(name = self.rol.opciones).first()       # pylint: disable=maybe-no-member
                print(grupo)
                if grupo:
                    self.groups.add(grupo)          # pylint: disable=maybe-no-member
                super().save(*args,**kwargs)
        else:
            if self.rol is not None:
                grupo_antiguo = Usuario.objects.filter(id = self.id).values('rol__opciones').first()     # pylint: disable=maybe-no-member
                
                if grupo_antiguo['rol__opciones'] == self.rol.opciones:           # pylint: disable=maybe-no-member
                    print("Entro en igualdad de roles")
                    super().save(*args,**kwargs)
                else:
                    grupo_anterior = Group.objects.filter(name = grupo_antiguo['rol__opciones']).first()                    
                    if grupo_anterior:
                        print(grupo_anterior)
                        self.groups.remove(grupo_anterior)          # pylint: disable=maybe-no-member
                    nuevo_grupo = Group.objects.filter(name = self.rol.opciones).first()     # pylint: disable=maybe-no-member
                    if nuevo_grupo:
                        self.groups.add(nuevo_grupo)    # pylint: disable=maybe-no-member
                    super().save(*args,**kwargs)


class GerenteGeneral(Usuario):
    
    class Meta:
        
        verbose_name = 'gerente general'
        verbose_name_plural = 'gerentes generales'

    def __str__(self):
        return self.username 
    
    def clean(self):
        
        query = Rol.objects.filter(opciones = 'GERENTE GENERAL')
        gerente = ""
        for obj in query:
            gerente = obj.id
        
        gerentes = Usuario.objects.filter(rol = gerente)
        
        if len(gerentes) == 1:
            raise ValidationError('Solo puedes registrar un único gerente general.')
    
        if self.rol.opciones != 'GERENTE GENERAL':
         raise ValidationError('El rol debe ser GERENTE GENERAL')

class Supervisor(Usuario):
    
    sucursal = models.ForeignKey(Sucursal, on_delete=models.PROTECT)
    
    
    class Meta:
        
        verbose_name = 'supervisor'
        verbose_name_plural = 'supervisores'
        
    def __str__(self):
        return self.username
    
    def clean(self):
        
     if self.rol.opciones != 'SUPERVISOR':
         raise ValidationError('El rol debe ser SUPERVISOR')

class Vendedor(Usuario):
    
    sucursal = models.ForeignKey(Sucursal, on_delete=models.PROTECT)
    
    class Meta:
        
        verbose_name = 'vendedor'
        verbose_name_plural = 'vendedores'
    
    def __str__(self):
        return self.username
    
    def clean(self):
        
     if self.rol.opciones != 'VENDEDOR':
         raise ValidationError('El rol debe ser VENDEDOR')
    
class Cajero(Usuario):
    
    sucursal = models.ForeignKey(Sucursal, on_delete=models.PROTECT)
    
    class Meta:
        
        verbose_name = 'cajero'
        verbose_name_plural = 'cajeros'
    
    def __str__(self):
        return self.username
    
    def clean(self):
        
     if self.rol.opciones != 'CAJERO':
         raise ValidationError('El rol debe ser CAJERO')
    
class Administrativo(Usuario):
    
    sucursal = models.ForeignKey(Sucursal, on_delete=models.PROTECT)
    
    class Meta:
        
        verbose_name = 'administrativo'
        verbose_name_plural = 'administrativos'
    
    def __str__(self):
        return self.username
    
    def clean(self):
        
     if self.rol.opciones != 'ADMINISTRATIVO':
         raise ValidationError('El rol debe ser ADMINISTRATIVO')
     
     

def defaultActivoUsuario(sender, instance, **kwargs):
    
    
    estados = EstadoUsuario.objects.all()
    if len(estados) > 0:
        if instance.estado_id == None:
            
            estadosQuery = EstadoUsuario.objects.filter(opciones = 'ACTIVO')
            activo = ""
            for estado in estadosQuery:
                activo = estado.id 
            
            instance.estado_id = activo 
            
            
pre_save.connect(defaultActivoUsuario, sender = Usuario)

def defaultActivoVendedor(sender, instance, **kwargs):
    
    
    estados = EstadoUsuario.objects.all()
    if len(estados) > 0:
        if instance.estado_id == None:
            
            estadosQuery = EstadoUsuario.objects.filter(opciones = 'ACTIVO')
            activo = ""
            for estado in estadosQuery:
                activo = estado.id 
            
            instance.estado_id = activo
           
            
pre_save.connect(defaultActivoVendedor, sender = Vendedor)

def defaultActivoSupervisor(sender, instance, **kwargs):
    
    
    estados = EstadoUsuario.objects.all()
    if len(estados) > 0:
        if instance.estado_id == None:
            
            estadosQuery = EstadoUsuario.objects.filter(opciones = 'ACTIVO')
            activo = ""
            for estado in estadosQuery:
                activo = estado.id 
            
            instance.estado_id = activo
    
            
pre_save.connect(defaultActivoSupervisor, sender = Supervisor)


def defaultActivoGerenteGeneral(sender, instance, **kwargs):
    
    
    estados = EstadoUsuario.objects.all()
    if len(estados) > 0:
        if instance.estado_id == None:
            
            estadosQuery = EstadoUsuario.objects.filter(opciones = 'ACTIVO')
            activo = ""
            for estado in estadosQuery:
                activo = estado.id 
            
            instance.estado_id = activo

            
pre_save.connect(defaultActivoGerenteGeneral, sender = GerenteGeneral)

def defaultActivoCajero(sender, instance, **kwargs):
    
    
    estados = EstadoUsuario.objects.all()
    if len(estados) > 0:
        if instance.estado_id == None:
            
            estadosQuery = EstadoUsuario.objects.filter(opciones = 'ACTIVO')
            activo = ""
            for estado in estadosQuery:
                activo = estado.id 
            
            instance.estado_id = activo 
        
            
pre_save.connect(defaultActivoCajero, sender = Cajero)

def defaultActivoAdministrativo(sender, instance, **kwargs):
    
    
    estados = EstadoUsuario.objects.all()
    if len(estados) > 0:
        if instance.estado_id == None:
            
            estadosQuery = EstadoUsuario.objects.filter(opciones = 'ACTIVO')
            activo = ""
            for estado in estadosQuery:
                activo = estado.id 
            
            instance.estado_id = activo
     
            
pre_save.connect(defaultActivoAdministrativo, sender = Administrativo)
    