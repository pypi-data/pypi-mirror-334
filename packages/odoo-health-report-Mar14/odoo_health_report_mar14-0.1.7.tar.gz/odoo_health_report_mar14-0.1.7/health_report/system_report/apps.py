from django.apps import AppConfig


class SystemReportConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'system_report'
    def ready(self) -> None:
        from health_report.urls import urlpatterns, include, path

        urlpatterns.append(
            path("", include("system_report.urls")),
        )
        return super().ready()