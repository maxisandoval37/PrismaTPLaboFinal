# Generated by Django 3.1.7 on 2021-06-07 02:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('presupuesto', '0001_initial'),
        ('usuario', '0001_initial'),
        ('item', '0001_initial'),
        ('sucursal', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='presupuesto',
            name='vendedor_asociado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='usuario.vendedor'),
        ),
        migrations.AddField(
            model_name='itempresupuesto',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='item.item'),
        ),
        migrations.AddField(
            model_name='itempresupuesto',
            name='presupuesto_asociado',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='presupuesto.presupuesto'),
        ),
        migrations.AddField(
            model_name='itempresupuesto',
            name='sucursal_asociada',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='sucursal.sucursal'),
        ),
    ]
