from django.apps import AppConfig


class HiringConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.hiring'

    def ready(self):
        from apps.hiring import signals
