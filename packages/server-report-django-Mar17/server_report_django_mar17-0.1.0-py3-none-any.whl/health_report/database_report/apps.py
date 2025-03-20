from django.apps import AppConfig


class DatabaseReportConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'database_report'
    def ready(self) -> None:
        from health_report.urls import urlpatterns, include, path

        urlpatterns.append(
            path("", include("database_report.urls")),
        )
        return super().ready()
