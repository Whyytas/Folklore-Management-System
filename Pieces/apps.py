from django.apps import AppConfig

class PiecesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Pieces'

    def ready(self):
        import Pieces.signals  # 👈 Register signals
