# Generated by Django 3.1.7 on 2021-05-17 01:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0002_auto_20210516_0602'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedidos',
            name='cantidad',
            field=models.IntegerField(null=True, verbose_name='Cantidad'),
        ),
        migrations.AddField(
            model_name='pedidos',
            name='solicitado',
            field=models.IntegerField(default=5, verbose_name='Solicitado: 5'),
        ),
    ]