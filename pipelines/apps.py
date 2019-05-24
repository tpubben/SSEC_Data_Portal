from django.apps import AppConfig
from django.contrib.admin.apps import AdminConfig


class PipelinesConfig(AppConfig):
    name = 'pipelines'

class PipelineAdminConfig(AdminConfig):
    default_site = 'pipelines.admin.CustomUserAdmin'