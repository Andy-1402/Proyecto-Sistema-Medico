# Generated by Django 4.2.16 on 2024-11-21 06:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_usuario', models.CharField(choices=[('CLIENTE', 'Cliente'), ('DOCTOR', 'Doctor'), ('RECEPCIONISTA', 'Recepcionista')], max_length=15)),
                ('telefono', models.CharField(blank=True, max_length=20, null=True)),
                ('direccion', models.TextField(blank=True, null=True)),
                ('foto', models.ImageField(blank=True, default='img/usuario_anonimo.png', upload_to='usuarios/', verbose_name='Foto')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
