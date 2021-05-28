# Generated by Django 3.1.7 on 2021-05-28 23:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cuit', models.CharField(max_length=11, unique=True, verbose_name='Cuit')),
                ('razon_social', models.CharField(max_length=20, unique=True, verbose_name='Razón Social')),
                ('email', models.EmailField(max_length=30, unique=True, verbose_name='Correo electronico')),
                ('telefono', models.CharField(max_length=13, null=True, unique=True, verbose_name='Telefono')),
                ('calle', models.CharField(blank=True, max_length=20, null=True, verbose_name='Calle')),
                ('numero', models.CharField(blank=True, max_length=4, null=True, verbose_name='Numero')),
                ('localidad', models.CharField(blank=True, max_length=20, null=True, verbose_name='Localidad')),
                ('provincia', models.CharField(blank=True, max_length=20, null=True, verbose_name='Provincia')),
                ('cod_postal', models.CharField(blank=True, max_length=4, null=True, verbose_name='Código postal')),
            ],
            options={
                'verbose_name': 'proveedor',
                'verbose_name_plural': 'proveedores',
            },
        ),
    ]
