from django.apps import AppConfig


class AttentionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'aplication.attention'

    def ready(self):
        import aplication.attention.signals 