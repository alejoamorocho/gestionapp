from django.apps import AppConfig


class DocumentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.documents'
    verbose_name = 'Gestión de Documentos'

    def ready(self):
        try:
            import apps.documents.signals
        except ImportError:
            pass
