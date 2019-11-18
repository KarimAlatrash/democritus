from django.apps import AppConfig

from django.contrib.admin.apps import AdminConfig


class DemocritusConfig(AppConfig):
    name = 'Democritus'


class AdministratorConfig(AdminConfig):
    default_site = 'Democritus.admin.DemocritusAdmin'
