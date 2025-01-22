from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoriaDocumentoViewSet, DocumentoViewSet,
    VersionDocumentoViewSet, PermisoDocumentoViewSet,
    HistorialAccesoViewSet
)

router = DefaultRouter()
router.register(r'categorias', CategoriaDocumentoViewSet)
router.register(r'documentos', DocumentoViewSet, basename='documento')
router.register(r'versiones', VersionDocumentoViewSet)
router.register(r'permisos', PermisoDocumentoViewSet)
router.register(r'historial', HistorialAccesoViewSet, basename='historial')

app_name = 'documents'

urlpatterns = [
    path('', include(router.urls)),
]
