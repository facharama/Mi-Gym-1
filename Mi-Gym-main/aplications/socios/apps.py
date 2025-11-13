from django.apps import AppConfig


class SociosConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "aplications.socios"
    def ready(self):
        import aplications.socios.signals
