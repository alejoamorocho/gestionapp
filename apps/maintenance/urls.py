from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PlanMantenimientoViewSet, MantenimientoViewSet,
    FotoMantenimientoViewSet, RepuestoUsadoViewSet
)

router = DefaultRouter()
router.register('planes', PlanMantenimientoViewSet)
router.register('mantenimientos', MantenimientoViewSet)
router.register('fotos', FotoMantenimientoViewSet)
router.register('repuestos', RepuestoUsadoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
