# Generated by Django 3.1.7 on 2021-06-18 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0003_auto_20210618_0439'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedidos',
            name='solicitado',
            field=models.IntegerField(default=66, verbose_name='Solicitado '),
        ),
    ]