from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EventoViewSet, AsistenteViewSet, MaterialEventoViewSet,
    CertificadoViewSet, EvaluacionViewSet
)

router = DefaultRouter()
router.register('eventos', EventoViewSet)
router.register('asistentes', AsistenteViewSet)
router.register('materiales', MaterialEventoViewSet)
router.register('certificados', CertificadoViewSet)
router.register('evaluaciones', EvaluacionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
