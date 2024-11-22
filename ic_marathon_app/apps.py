from django.apps import AppConfig


class IcMarathonAppConfig(AppConfig):
    name = 'ic_marathon_app'

    def ready(self):
        import ic_marathon_app.signals