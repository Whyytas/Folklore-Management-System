from django.apps import AppConfig

class KuriniaiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Kuriniai'

    def ready(self):
        import Kuriniai.signals  # 👈 Register signals
