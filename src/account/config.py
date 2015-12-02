from django.apps import AppConfig


class DataHubAccountConfig(AppConfig):
    name = 'account'
    verbose_name = 'DataHub Accounts'

    def ready(self):
        import signals
