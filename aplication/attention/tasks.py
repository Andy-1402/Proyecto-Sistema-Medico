from celery import shared_task
from django.core.mail import send_mail
from django.utils.timezone import now, timedelta
from .models import CitaMedica

@shared_task
def enviar_recordatorio_citas():
    hoy = now().date()
    citas = CitaMedica.objects.filter(fecha__in=[hoy + timedelta(days=2), hoy])
    for cita in citas:
        paciente_email = cita.paciente.email
        asunto = f"Recordatorio: Cita médica el {cita.fecha.strftime('%d/%m/%Y')} a las {cita.hora_cita.strftime('%H:%M')}"
        mensaje = (
            f"Estimado/a {cita.paciente.nombre_completo},\n\n"
            f"Le recordamos que tiene una cita médica programada:\n"
            f"- Fecha: {cita.fecha.strftime('%d/%m/%Y')}\n"
            f"- Hora: {cita.hora_cita.strftime('%H:%M')}\n\n"
            "Por favor, no falte a su cita.\n"
        )
        send_mail(
            asunto,
            mensaje,
            'sistema.medico2024@gmail.com',
            [paciente_email],
            fail_silently=False,
        )
