# Generated by Django 3.1.7 on 2021-05-31 19:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sucursal', '0001_initial'),
        ('cliente', '0001_initial'),
        ('proveedor', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('opciones', models.CharField(choices=[('Útiles de Construcción', 'Utiles De Construccion'), ('Revestimientos', 'Revestimientos'), ('Confort y Domótica', 'Confort Y Domotica'), ('Iluminación', 'Iluminacion'), ('Material de instalación', 'Material De Instalacion'), ('Bombillas y tubos', 'Bombillas Y Tubos'), ('Maquinaria', 'Maquinaria'), ('Herramienta manual', 'Herramienta Manual'), ('Equipo de protección individual', 'Equipo De Proteccion Individual'), ('Ordenación de herramientas', 'Ordenacion De Herramientas'), ('Aparatos sanitarios', 'Aparatos Sanitarios'), ('Complementos de baño', 'Complementos De Bano'), ('Grifería', 'Griferia'), ('Riego', 'Riego'), ('Decoración de jardín', 'Decoracion Jardin'), ('Cerrajería', 'Cerrajeria'), ('Pintura', 'Pintura'), ('Pilas', 'Pilas')], max_length=40)),
                ('prov_preferido', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='proveedor.proveedor')),
            ],
        ),
        migrations.CreateModel(
            name='Estado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('opciones', models.CharField(choices=[('ACTIVO', 'Activo'), ('INACTIVO', 'Inactivo'), ('PENDIENTE', 'Pendiente'), ('DESCONTINUADO', 'Descontinuado')], max_length=13)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50, unique=True, verbose_name='Nombre')),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='Precio')),
                ('descripcion', models.CharField(blank=True, max_length=50, null=True, verbose_name='Descripción')),
                ('stockminimo', models.IntegerField(default=1, verbose_name='Stock Minimo')),
                ('stockseguridad', models.IntegerField(default=0, verbose_name='Stock de Seguridad')),
                ('ubicacion', models.CharField(max_length=15, verbose_name='Ubicación')),
                ('ultima_modificacion', models.DateTimeField(blank=True, null=True, verbose_name='Ultima Modificación')),
                ('repo_por_lote', models.BooleanField(verbose_name='Reposición por Lote')),
                ('cantidad', models.IntegerField(default=0, verbose_name='Cantidad')),
                ('solicitud', models.BooleanField(default=False)),
                ('reintentos', models.IntegerField(default=0)),
                ('cantidad_lote', models.PositiveIntegerField(default=0, null=True, verbose_name='Cantidad de reposición por lote')),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='item.categoria')),
                ('estado', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='item.estado')),
            ],
            options={
                'verbose_name': 'item',
                'verbose_name_plural': 'items',
            },
        ),
        migrations.CreateModel(
            name='UnidadDeMedida',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('opciones', models.CharField(choices=[('TONELADA', 'Tonelada'), ('KG', 'Kg'), ('GR', 'Gr'), ('MG', 'Mg'), ('LT', 'Lt'), ('ML', 'Ml'), ('M', 'M'), ('CM', 'Cm'), ('MM', 'Mm')], max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name='SubCategoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('opciones', models.CharField(choices=[('Carretillas', 'Carretillas'), ('Andamios', 'Andamios'), ('Elevadores', 'Elevadores'), ('Cerámica', 'Ceramica'), ('Piedra natural', 'Pieda Natural'), ('Perfilería y accesorios', 'Perfileria Y Accesorios'), ('Termostatos', 'Termostatos'), ('Timbres', 'Timbres'), ('Apertura motorizada', 'Apertura Motorizada'), ('Linternas', 'Linternas'), ('Focos', 'Focos'), ('Pantallas', 'Pantallas'), ('Cable', 'Cable'), ('Terminales', 'Terminales'), ('Magnetotérmicos y fusibles', 'Magnetotermicos Y Fusibles'), ('Bombillas led', 'Bombillas Led'), ('Bombillas incandescentes', 'Bombillas Incandescentes'), ('Bombillas bajo consumo', 'Bombillas Bajo Consumo'), ('Hidrolavadores', 'Hidrolavadores'), ('Aspiradores', 'Aspiradores'), ('Compresores', 'Compresores'), ('Motores', 'Motores'), ('Generadores', 'Generadores'), ('Alicates y tenazas', 'Alicates Y Tenazas'), ('Llaves', 'Llaves'), ('Destornilladores', 'Destornilladores'), ('Herramientas de albañilería', 'Herramientas Albanileria'), ('Guantes', 'Guantes'), ('Protección visual', 'Proteccion Visual'), ('Protección auditiva', 'Proteccion Auditiva'), ('Protección anticaidas', 'Proteccion Anticaidas'), ('Cajas y maletas', 'Cajas Y Maletas'), ('Cinturones portaherramientas', 'Cinturones Portaherramientas'), ('Carros', 'Carros'), ('Lavabo pedestal', 'Lavabo Pedestal'), ('Lavamanos', 'Lavamanos'), ('Cisternas', 'Cisternas'), ('Cristal', 'Cristal'), ('Porcelana', 'Porcelana'), ('Madera', 'Madera'), ('Termostáticos', 'Termostaticos'), ('Monobloc', 'Monobloc'), ('Monomando', 'Monomando'), ('Mangueras', 'Mangueras'), ('Difusores', 'Difusores'), ('Regaderas', 'Regaderas'), ('Macetas', 'Macetas'), ('Estanques', 'Estanques'), ('Fuentes', 'Fuentes'), ('Cerraduras para puertas', 'Cerraduras Para Puertas'), ('Sistemas antirrobo', 'Sistemas Antirrobo'), ('Cerraduras electrónicas', 'Cerraduras Electronicas'), ('Interior', 'Interior'), ('Exterior', 'Exterior'), ('Rodillos', 'Rodillos'), ('Pinceles', 'Pinceles'), ('Pilas recargables', 'Pilas Recargables'), ('Pilas no recargables', 'Pilas No Recargables')], max_length=40)),
                ('nombre_categoria', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='item.categoria')),
            ],
        ),
        migrations.CreateModel(
            name='Pedidos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField(null=True, verbose_name='Cantidad')),
                ('solicitado', models.IntegerField(default=53, verbose_name='Solicitado 53')),
                ('cuenta_corriente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cliente.cuentacorriente')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='item.item')),
                ('proveedor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='proveedor.proveedor')),
                ('sucursal', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='sucursal.sucursal')),
            ],
            options={
                'verbose_name': 'pedido',
                'verbose_name_plural': 'pedidos',
            },
        ),
        migrations.AddField(
            model_name='item',
            name='subcategoria',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='item.subcategoria'),
        ),
        migrations.AddField(
            model_name='item',
            name='sucursal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='sucursal.sucursal'),
        ),
        migrations.AddField(
            model_name='item',
            name='unidad_de_medida',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='item.unidaddemedida'),
        ),
    ]
