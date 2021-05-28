# Generated by Django 3.1.7 on 2021-05-28 23:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sucursal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=4, unique=True)),
                ('idCasaCentral', models.IntegerField(default=1)),
                ('calle', models.CharField(max_length=20, verbose_name='Calle')),
                ('numero', models.CharField(max_length=4, verbose_name='Numero')),
                ('localidad', models.CharField(max_length=20, null=True, verbose_name='Localidad')),
                ('provincia', models.CharField(max_length=20, null=True, verbose_name='Provincia')),
                ('cod_postal', models.CharField(max_length=4, verbose_name='Código postal')),
            ],
            options={
                'verbose_name': 'sucursal',
                'verbose_name_plural': 'sucursales',
            },
        ),
        migrations.CreateModel(
            name='Caja',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=4, unique=True, verbose_name='Identificador')),
                ('saldo_disponible', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Saldo Disponible')),
                ('egresos', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Egresos')),
                ('ingresos', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Ingresos')),
                ('saldo_inicial', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Saldo Inicial')),
                ('saldo_final', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Saldo Final')),
                ('sucursal_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='sucursal.sucursal')),
            ],
            options={
                'verbose_name': 'caja',
                'verbose_name_plural': 'cajas',
            },
        ),
    ]
