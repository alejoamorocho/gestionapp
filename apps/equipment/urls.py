from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoriaViewSet, FabricanteViewSet, EquipoViewSet,
    ImagenEquipoViewSet, DocumentoEquipoViewSet, HistorialPrecioViewSet
)

router = DefaultRouter()
router.register('categorias', CategoriaViewSet)
router.register('fabricantes', FabricanteViewSet)
router.register('equipos', EquipoViewSet)
router.register('imagenes', ImagenEquipoViewSet)
router.register('documentos', DocumentoEquipoViewSet)
router.register('historial-precios', HistorialPrecioViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
