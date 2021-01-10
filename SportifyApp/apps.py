from django.apps import AppConfig


class SportifyappConfig(AppConfig):
    name = 'SportifyApp'

    def ready(self):
        import SportifyApp.signals