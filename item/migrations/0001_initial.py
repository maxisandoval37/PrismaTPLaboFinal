# Generated by Django 3.1.7 on 2021-06-18 07:10

from django.db import migrations, models
import django.db.models.deletion
import item.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('opciones', models.CharField(choices=[('Útiles de Construcción', 'Utiles De Construccion'), ('Revestimientos', 'Revestimientos'), ('Confort y Domótica', 'Confort Y Domotica'), ('Iluminación', 'Iluminacion'), ('Material de instalación', 'Material De Instalacion'), ('Bombillas y tubos', 'Bombillas Y Tubos'), ('Maquinaria', 'Maquinaria'), ('Herramienta manual', 'Herramienta Manual'), ('Equipo de protección individual', 'Equipo De Proteccion Individual'), ('Ordenación de herramientas', 'Ordenacion De Herramientas'), ('Aparatos sanitarios', 'Aparatos Sanitarios'), ('Complementos de baño', 'Complementos De Bano'), ('Grifería', 'Griferia'), ('Riego', 'Riego'), ('Decoración de jardín', 'Decoracion Jardin'), ('Cerrajería', 'Cerrajeria'), ('Pintura', 'Pintura'), ('Pilas', 'Pilas')], max_length=40)),
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
            name='HistorialPref',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de asignación')),
            ],
            options={
                'verbose_name': 'historial de preferenciados',
                'verbose_name_plural': 'historiales de preferenciados',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('codigo_de_barras', models.BigIntegerField(default=item.models.random_codigo, unique=True, verbose_name='Código de barras')),
                ('nombre', models.CharField(max_length=50, verbose_name='Nombre')),
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
            ],
            options={
                'verbose_name': 'item',
                'verbose_name_plural': 'items',
            },
        ),
        migrations.CreateModel(
            name='Mezcla',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad_primera_pintura', models.IntegerField(verbose_name='Cantidad de la primera pintura (En mililitros)')),
                ('cantidad_segunda_pintura', models.IntegerField(verbose_name='Cantidad de la segunda pintura (En mililitros)')),
            ],
            options={
                'verbose_name': 'mezcla',
                'verbose_name_plural': 'mezclas',
            },
        ),
        migrations.CreateModel(
            name='MezclaUsada',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad_primera_pintura', models.PositiveIntegerField(default=0, verbose_name='Cantidad de la primera pintura (En mililitros)')),
                ('cantidad_segunda_pintura', models.PositiveIntegerField(default=0, verbose_name='Cantidad de la segunda pintura (En mililitros)')),
            ],
            options={
                'verbose_name': 'mezcla',
                'verbose_name_plural': 'mezclas',
            },
        ),
        migrations.CreateModel(
            name='Pedidos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('cantidad', models.IntegerField(null=True, verbose_name='Cantidad')),
                ('solicitado', models.IntegerField(default=46, verbose_name='Solicitado ')),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=7, verbose_name='Total')),
            ],
            options={
                'verbose_name': 'pedido',
                'verbose_name_plural': 'pedidos',
            },
        ),
        migrations.CreateModel(
            name='PinturaNueva',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo_de_barras', models.BigIntegerField(default=item.models.random_codigo, unique=True, verbose_name='Código de barras')),
                ('nombre', models.CharField(max_length=30, verbose_name='Nombre de pintura')),
                ('color', models.CharField(max_length=50, verbose_name='Color de pintura')),
                ('cantidad', models.PositiveIntegerField(verbose_name='Cantidad de pintura (ML)')),
                ('stock', models.IntegerField(verbose_name='Stock')),
                ('pcant', models.PositiveIntegerField(verbose_name='Primera cantidad')),
                ('scant', models.PositiveIntegerField(verbose_name='Segunda cantidad')),
                ('precio', models.PositiveIntegerField(verbose_name='Precio')),
            ],
            options={
                'verbose_name': 'pintura nueva',
                'verbose_name_plural': 'pinturas nuevas',
            },
        ),
        migrations.CreateModel(
            name='PinturaUsada',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo_de_barras', models.BigIntegerField(default=item.models.random_codigo, unique=True, verbose_name='Código de barras')),
                ('nombre', models.CharField(max_length=30, verbose_name='Nombre de pintura')),
                ('color', models.CharField(max_length=50, verbose_name='Color de pintura')),
                ('cantidad_restante', models.PositiveIntegerField(verbose_name='Cantidad de pintura restante')),
                ('precio', models.PositiveIntegerField(verbose_name='Precio')),
            ],
            options={
                'verbose_name': 'pintura usada',
                'verbose_name_plural': 'pinturas usadas',
            },
        ),
        migrations.CreateModel(
            name='ReportePrecios',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de modificación')),
                ('aumento', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='Aumento')),
            ],
            options={
                'verbose_name': 'reporte de precios',
                'verbose_name_plural': 'reportes de precios',
            },
        ),
        migrations.CreateModel(
            name='ReportePreciosItems',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de modificación')),
                ('aumento', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='Aumento')),
            ],
            options={
                'verbose_name': 'reporte de precios global',
                'verbose_name_plural': 'reportes de precios globales',
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
            name='Pintura',
            fields=[
                ('item_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='item.item')),
                ('color', models.CharField(max_length=30, verbose_name='Color')),
                ('cantidad_pintura', models.PositiveIntegerField(default=0, verbose_name='Cantidad de pintura')),
            ],
            options={
                'verbose_name': 'pintura',
                'verbose_name_plural': 'pinturas',
            },
            bases=('item.item',),
        ),
        migrations.CreateModel(
            name='SubCategoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('opciones', models.CharField(choices=[('Carretillas', 'Carretillas'), ('Andamios', 'Andamios'), ('Elevadores', 'Elevadores'), ('Cerámica', 'Ceramica'), ('Piedra natural', 'Pieda Natural'), ('Perfilería y accesorios', 'Perfileria Y Accesorios'), ('Termostatos', 'Termostatos'), ('Timbres', 'Timbres'), ('Apertura motorizada', 'Apertura Motorizada'), ('Linternas', 'Linternas'), ('Focos', 'Focos'), ('Pantallas', 'Pantallas'), ('Cable', 'Cable'), ('Terminales', 'Terminales'), ('Magnetotérmicos y fusibles', 'Magnetotermicos Y Fusibles'), ('Bombillas led', 'Bombillas Led'), ('Bombillas incandescentes', 'Bombillas Incandescentes'), ('Bombillas bajo consumo', 'Bombillas Bajo Consumo'), ('Hidrolavadores', 'Hidrolavadores'), ('Aspiradores', 'Aspiradores'), ('Compresores', 'Compresores'), ('Motores', 'Motores'), ('Generadores', 'Generadores'), ('Alicates y tenazas', 'Alicates Y Tenazas'), ('Llaves', 'Llaves'), ('Destornilladores', 'Destornilladores'), ('Herramientas de albañilería', 'Herramientas Albanileria'), ('Guantes', 'Guantes'), ('Protección visual', 'Proteccion Visual'), ('Protección auditiva', 'Proteccion Auditiva'), ('Protección anticaidas', 'Proteccion Anticaidas'), ('Cajas y maletas', 'Cajas Y Maletas'), ('Cinturones portaherramientas', 'Cinturones Portaherramientas'), ('Carros', 'Carros'), ('Lavabo pedestal', 'Lavabo Pedestal'), ('Lavamanos', 'Lavamanos'), ('Cisternas', 'Cisternas'), ('Cristal', 'Cristal'), ('Porcelana', 'Porcelana'), ('Madera', 'Madera'), ('Termostáticos', 'Termostaticos'), ('Monobloc', 'Monobloc'), ('Monomando', 'Monomando'), ('Mangueras', 'Mangueras'), ('Difusores', 'Difusores'), ('Regaderas', 'Regaderas'), ('Macetas', 'Macetas'), ('Estanques', 'Estanques'), ('Fuentes', 'Fuentes'), ('Cerraduras para puertas', 'Cerraduras Para Puertas'), ('Sistemas antirrobo', 'Sistemas Antirrobo'), ('Cerraduras electrónicas', 'Cerraduras Electronicas'), ('Interior', 'Interior'), ('Exterior', 'Exterior'), ('Rodillos', 'Rodillos'), ('Pinceles', 'Pinceles'), ('Pilas recargables', 'Pilas Recargables'), ('Pilas no recargables', 'Pilas No Recargables')], max_length=40)),
                ('nombre_categoria', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='item.categoria')),
            ],
        ),
    ]
