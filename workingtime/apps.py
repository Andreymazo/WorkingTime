from django.apps import AppConfig


class WorkingtimeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'workingtime'

    def ready(self):
        import workingtime.signals
