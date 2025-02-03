from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Perfil


# Esta es la función que se ejecutará después de guardar un objeto User.
# Está conectada al evento 'post_save', lo que significa que se ejecuta después de que un usuario es guardado en la base de datos.

@receiver(post_save, sender=User)
def crear_o_actualizar_perfil(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(user=instance)          # Si el usuario es nuevo, creamos un perfil asociado a este usuario.
    instance.perfil.save()                            # 'instance' es el usuario recién creado.
    
    
#Esta función garantiza que cada vez que se crea un usuario (User), automáticamente se cree un
#objeto Perfil asociado a ese usuario. Si el perfil ya existe (por ejemplo, cuando se actualiza un
#usuario), el perfil se guarda para reflejar cualquier cambio en el usuario.
#