import os
from celery import Celery

# Establece la configuración predeterminada de Django para Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'doctor.settings')

app = Celery('doctor')

# Configura Celery para leer las configuraciones desde las variables que comienzan con "CELERY"
app.config_from_object('django.conf:settings', namespace='CELERY')

# Descubre automáticamente tareas en las aplicaciones instaladas
app.autodiscover_tasks()
