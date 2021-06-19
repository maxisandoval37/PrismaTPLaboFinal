# Generated by Django 3.1.7 on 2021-06-18 07:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sucursal', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(max_length=20, unique=True, verbose_name='Nombre de usuario')),
                ('email', models.EmailField(max_length=30, unique=True, verbose_name='Correo Electrónico')),
                ('cuit', models.CharField(max_length=11, unique=True, verbose_name='Cuit')),
                ('nombre', models.CharField(max_length=16, null=True, verbose_name='Nombre')),
                ('apellido', models.CharField(max_length=16, null=True, verbose_name='Apellido')),
                ('telefono', models.CharField(max_length=13, null=True, verbose_name='Telefono')),
                ('calle', models.CharField(blank=True, max_length=20, null=True, verbose_name='Calle')),
                ('numero', models.CharField(blank=True, max_length=4, null=True, verbose_name='Numero')),
                ('localidad', models.CharField(blank=True, max_length=20, null=True, verbose_name='Localidad')),
                ('provincia', models.CharField(blank=True, max_length=20, null=True, verbose_name='Provincia')),
                ('cod_postal', models.CharField(blank=True, max_length=4, null=True, verbose_name='Código postal')),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Estado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('opciones', models.CharField(choices=[('ACTIVO', 'Activo'), ('INACTIVO', 'Inactivo')], default='ACTIVO', max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name='Rol',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('opciones', models.CharField(choices=[('SUPERVISOR', 'Supervisor'), ('GERENTE GENERAL', 'Gerente General'), ('VENDEDOR', 'Vendedor'), ('ADMINISTRATIVO', 'Administrativo'), ('CAJERO', 'Cajero')], max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='GerenteGeneral',
            fields=[
                ('usuario_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='usuario.usuario')),
            ],
            options={
                'verbose_name': 'gerente general',
                'verbose_name_plural': 'gerentes generales',
            },
            bases=('usuario.usuario',),
        ),
        migrations.AddField(
            model_name='usuario',
            name='estado',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='usuario.estado'),
        ),
        migrations.AddField(
            model_name='usuario',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='usuario',
            name='rol',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='usuario.rol'),
        ),
        migrations.AddField(
            model_name='usuario',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
        migrations.CreateModel(
            name='Vendedor',
            fields=[
                ('usuario_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='usuario.usuario')),
                ('sucursal', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='sucursal.sucursal')),
            ],
            options={
                'verbose_name': 'vendedor',
                'verbose_name_plural': 'vendedores',
            },
            bases=('usuario.usuario',),
        ),
        migrations.CreateModel(
            name='Supervisor',
            fields=[
                ('usuario_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='usuario.usuario')),
                ('sucursal', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='sucursal.sucursal')),
            ],
            options={
                'verbose_name': 'supervisor',
                'verbose_name_plural': 'supervisores',
            },
            bases=('usuario.usuario',),
        ),
        migrations.CreateModel(
            name='Cajero',
            fields=[
                ('usuario_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='usuario.usuario')),
                ('sucursal', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='sucursal.sucursal')),
            ],
            options={
                'verbose_name': 'cajero',
                'verbose_name_plural': 'cajeros',
            },
            bases=('usuario.usuario',),
        ),
        migrations.CreateModel(
            name='Administrativo',
            fields=[
                ('usuario_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='usuario.usuario')),
                ('sucursal', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='sucursal.sucursal')),
            ],
            options={
                'verbose_name': 'administrativo',
                'verbose_name_plural': 'administrativos',
            },
            bases=('usuario.usuario',),
        ),
    ]
