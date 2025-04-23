from django.apps import AppConfig


class WinConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'win'

    def ready(self):
    # Импортируем сигналы при запуске приложения
        from . import signals