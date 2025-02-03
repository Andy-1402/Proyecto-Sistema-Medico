import resend
from django.conf import settings

# Configura la clave de API
resend.api_key = settings.RESEND_API_KEY

def enviar_email_resend(destinatarios, asunto, contenido_html, contenido_texto=None):
    """
    Envía un correo electrónico usando la API de Resend.
    """
    try:
        response = resend.Emails.send(
            {
                "from": settings.DEFAULT_FROM_EMAIL,
                "to": destinatarios,
                "subject": asunto,
                "html": contenido_html,
                "text": contenido_texto if contenido_texto else contenido_html,
            }
        )
        return response
    except Exception as e:
        # Manejo de errores
        print(f"Error enviando el correo: {e}")
        return None
