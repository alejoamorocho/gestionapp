from django.shortcuts import render
from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import PlanMantenimiento, Mantenimiento, FotoMantenimiento, RepuestoUsado
from .serializers import (
    PlanMantenimientoSerializer,
    MantenimientoListSerializer, MantenimientoDetailSerializer, MantenimientoCreateUpdateSerializer,
    FotoMantenimientoSerializer, RepuestoUsadoSerializer
)

# Create your views here.

class PlanMantenimientoViewSet(viewsets.ModelViewSet):
    queryset = PlanMantenimiento.objects.all()
    serializer_class = PlanMantenimientoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['equipo', 'frecuencia', 'activo', 'requiere_tecnico_especializado']
    search_fields = ['nombre', 'descripcion', 'procedimiento']
    ordering_fields = ['nombre', 'frecuencia', 'fecha_creacion']

class MantenimientoViewSet(viewsets.ModelViewSet):
    queryset = Mantenimiento.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['equipo', 'tipo', 'estado', 'tecnico_asignado', 'requiere_seguimiento']
    search_fields = ['titulo', 'descripcion', 'diagnostico', 'trabajo_realizado']
    ordering_fields = ['fecha_programada', 'fecha_inicio', 'fecha_fin']

    def get_serializer_class(self):
        if self.action == 'list':
            return MantenimientoListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return MantenimientoCreateUpdateSerializer
        return MantenimientoDetailSerializer

    def perform_create(self, serializer):
        # Si el mantenimiento está basado en un plan, copiar la información relevante
        plan = serializer.validated_data.get('plan')
        if plan:
            serializer.save(
                equipo=plan.equipo,
                descripcion=plan.procedimiento,
                tipo='PREVENTIVO'
            )
        else:
            serializer.save()

class FotoMantenimientoViewSet(viewsets.ModelViewSet):
    queryset = FotoMantenimiento.objects.all()
    serializer_class = FotoMantenimientoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['mantenimiento', 'tipo']
    search_fields = ['descripcion']
    ordering_fields = ['fecha_subida']

class RepuestoUsadoViewSet(viewsets.ModelViewSet):
    queryset = RepuestoUsado.objects.all()
    serializer_class = RepuestoUsadoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['mantenimiento']
    search_fields = ['nombre', 'numero_parte', 'proveedor']
    ordering_fields = ['nombre', 'numero_parte']
