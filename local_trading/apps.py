from django.apps import AppConfig


class LocalTradingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'local_trading'

    def ready(self):
        from local_trading import signals
