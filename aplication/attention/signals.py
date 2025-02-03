from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import CitaMedica

@receiver(post_save, sender=CitaMedica)
def enviar_notificacion_cita_creada(sender, instance, created, **kwargs):
    if created:
        paciente_email = instance.paciente.email  # Asegúrate de que el paciente tenga un email válido
        asunto = f"Cita médica programada: {instance.fecha} a las {instance.hora_cita}"
        mensaje = (
            f"Estimado/a {instance.paciente.nombre_completo},\n\n"
            f"Su cita médica ha sido programada con los siguientes detalles:\n"
            f"- Fecha: {instance.fecha.strftime('%d/%m/%Y')}\n"
            f"- Hora: {instance.hora_cita.strftime('%H:%M')}\n"
            f"- Estado: {instance.get_estado_display()}\n\n"
            "Por favor, póngase en contacto con nosotros si tiene alguna duda.\n"
        )
        send_mail(
            asunto,
            mensaje,
            'sistema.medico2024@gmail.com',  # Configurado en `settings.py`
            [paciente_email],
            fail_silently=False,
        )
