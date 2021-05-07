from .base import *

DEBUG = True

ALLOWED_HOSTS = ['localhost']


DATABASES = {
     'default': {
         'ENGINE':'django.db.backends.postgresql',
         'NAME': 'proyectoprisma',
         'USER': 'postgres',
         'PASSWORD': 'tomy1202',
         'HOST': 'localhost',
         'PORT':'5432',
        
     }
 }
 
#DATABASES = {
   # 'default': {
   #     'ENGINE': 'django.db.backends.sqlite3',
  #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
 #   }
#}