# models.py
from django.contrib.auth.models import User
from django.db import models

class Perfil(models.Model):
    TIPOS_USUARIO = (
        ('CLIENTE', 'Cliente'),
        ('DOCTOR', 'Doctor'),
        ('RECEPCIONISTA', 'Recepcionista'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo_usuario = models.CharField(max_length=15, choices=TIPOS_USUARIO)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    foto = models.ImageField(upload_to='usuarios/', verbose_name='Foto', default='img/usuario_anonimo.png', blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_tipo_usuario_display()}"
