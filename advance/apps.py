from django.apps import AppConfig


class AdvanceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'advance'

    def ready(self):
        import advance.signals  # <-- bu joy muhim!
