# Generated by Django 3.1.7 on 2021-06-17 22:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0001_initial'),
    ]

    operations = [
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
    ]
