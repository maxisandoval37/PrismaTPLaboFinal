from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']


DATABASES = {
     'default': {
         'ENGINE': 'django.db.backends.postgresql',
         'NAME': 'dae0gc7dnjalf',
         'USER': 'cfxvnrjbibqlqe',
         'PASSWORD': '3a80976555dc9b1e64eb70e05a4da94cfd10709f48e373a07fb042064be94a86',
         'HOST': 'ec2-35-174-35-242.compute-1.amazonaws.com',
         'PORT':'5432',
        
     }
 }