from django.apps import AppConfig


class LoginAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'login_app'

    def ready(self)-> None:
        from health_report.urls import urlpatterns, include, path
        urlpatterns.append(
            path('',include('login_app.urls'))
        )
        return super().ready()
