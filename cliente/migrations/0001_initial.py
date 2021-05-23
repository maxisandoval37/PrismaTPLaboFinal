# Generated by Django 3.1.7 on 2021-05-23 22:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CategoriaCliente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('opciones', models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C')], max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cuit', models.CharField(max_length=11, unique=True, verbose_name='Cuit')),
                ('nombre', models.CharField(max_length=20, null=True, verbose_name='Nombre')),
                ('apellido', models.CharField(max_length=20, null=True, verbose_name='Apellido')),
                ('email', models.EmailField(max_length=30, unique=True, verbose_name='Correo electronico')),
                ('telefono', models.CharField(max_length=13, unique=True, verbose_name='Telefono')),
                ('categoria_cliente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cliente.categoriacliente')),
            ],
        ),
        migrations.CreateModel(
            name='EstadoCliente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('opciones', models.CharField(choices=[('ACTIVO', 'Activo'), ('INACTIVO', 'Inactivo'), ('DEUDOR', 'Deudor'), ('INCOBRABLE', 'Incobrable')], max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='EstadoDeuda',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('opciones', models.CharField(choices=[('PAGA', 'Paga'), ('IMPAGA', 'Impaga')], max_length=6)),
            ],
        ),
        migrations.CreateModel(
            name='MedioDePago',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('opciones', models.CharField(choices=[('DÉBITO', 'Debito'), ('CRÉDITO', 'Credito'), ('TRANSFERENCIA', 'Transferencia'), ('MERCADOPAGO', 'Mercadopago'), ('EFECTIVO', 'Efectivo'), ('CHEQUE', 'Cheque')], max_length=13)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cliente.cliente')),
            ],
        ),
        migrations.CreateModel(
            name='Deuda',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dias', models.IntegerField(null=True, verbose_name='Dias')),
                ('monto', models.FloatField(null=True, verbose_name='Monto')),
                ('cliete_asociado', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cliente.cliente')),
                ('estado_deuda', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cliente.estadodeuda')),
            ],
        ),
        migrations.CreateModel(
            name='CuentaCorriente',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cliente.cliente')),
            ],
        ),
        migrations.AddField(
            model_name='cliente',
            name='estado_cliente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cliente.estadocliente'),
        ),
    ]
