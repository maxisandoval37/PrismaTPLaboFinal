# Generated by Django 3.1.7 on 2021-05-31 00:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venta', '0002_auto_20210530_1926'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venta',
            name='tipo_de_venta',
            field=models.CharField(blank=True, default='LOCAL', max_length=7, null=True, verbose_name='Tipo de venta'),
        ),
        migrations.DeleteModel(
            name='TipoVenta',
        ),
    ]
