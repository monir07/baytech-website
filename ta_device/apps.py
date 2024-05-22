from django.apps import AppConfig


class TaDeviceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ta_device'

    def ready(self):
        from ta_device import scheduler
        scheduler.start()
