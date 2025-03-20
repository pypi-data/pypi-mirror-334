from django.apps import AppConfig


class ModuleQualityConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'module_quality'

    def ready(self):
        from health_report.urls import urlpatterns, include, path
        urlpatterns.append(
            path('',include('module_quality.urls'))
        )
        return super().ready()
