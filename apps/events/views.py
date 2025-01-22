from django.shortcuts import render
from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Evento, Asistente, MaterialEvento, Certificado, Evaluacion
from .serializers import (
    EventoListSerializer, EventoDetailSerializer, EventoCreateUpdateSerializer,
    AsistenteListSerializer, AsistenteDetailSerializer, AsistenteCreateUpdateSerializer,
    MaterialEventoSerializer, CertificadoSerializer, EvaluacionSerializer
)

# Create your views here.

class EventoViewSet(viewsets.ModelViewSet):
    queryset = Evento.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['tipo', 'modalidad', 'activo', 'instructor']
    search_fields = ['titulo', 'descripcion', 'ubicacion']
    ordering_fields = ['fecha_inicio', 'fecha_fin', 'fecha_creacion']

    def get_serializer_class(self):
        if self.action == 'list':
            return EventoListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return EventoCreateUpdateSerializer
        return EventoDetailSerializer

class AsistenteViewSet(viewsets.ModelViewSet):
    queryset = Asistente.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['evento', 'estado', 'asistio', 'certificado_emitido']
    search_fields = ['usuario__first_name', 'usuario__last_name', 'usuario__email']
    ordering_fields = ['fecha_registro', 'fecha_confirmacion']

    def get_serializer_class(self):
        if self.action == 'list':
            return AsistenteListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return AsistenteCreateUpdateSerializer
        return AsistenteDetailSerializer

    def get_queryset(self):
        # Si el usuario es un instructor, ver solo sus eventos
        if self.request.user.tipo == 'TECNICO':
            return Asistente.objects.filter(evento__instructor=self.request.user)
        # Si es un usuario normal, ver solo sus registros
        elif self.request.user.tipo == 'CLIENTE':
            return Asistente.objects.filter(usuario=self.request.user)
        # Administradores ven todo
        return Asistente.objects.all()

class MaterialEventoViewSet(viewsets.ModelViewSet):
    queryset = MaterialEvento.objects.all()
    serializer_class = MaterialEventoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['evento', 'publico']
    search_fields = ['titulo', 'descripcion']
    ordering_fields = ['orden', 'fecha_subida']

    def get_queryset(self):
        queryset = MaterialEvento.objects.all()
        if self.request.user.tipo == 'CLIENTE':
            # Clientes solo ven materiales públicos o de eventos a los que están registrados
            return queryset.filter(
                models.Q(publico=True) |
                models.Q(evento__asistentes__usuario=self.request.user)
            ).distinct()
        return queryset

class CertificadoViewSet(viewsets.ModelViewSet):
    queryset = Certificado.objects.all()
    serializer_class = CertificadoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['asistente__evento', 'firmado_por']
    search_fields = ['numero_certificado', 'asistente__usuario__email']
    ordering_fields = ['fecha_emision']

    def get_queryset(self):
        if self.request.user.tipo == 'CLIENTE':
            return Certificado.objects.filter(asistente__usuario=self.request.user)
        return Certificado.objects.all()

class EvaluacionViewSet(viewsets.ModelViewSet):
    queryset = Evaluacion.objects.all()
    serializer_class = EvaluacionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['asistente__evento', 'aprobado', 'evaluador']
    search_fields = ['asistente__usuario__email', 'observaciones']
    ordering_fields = ['fecha_evaluacion']

    def get_queryset(self):
        if self.request.user.tipo == 'CLIENTE':
            return Evaluacion.objects.filter(asistente__usuario=self.request.user)
        elif self.request.user.tipo == 'TECNICO':
            return Evaluacion.objects.filter(
                models.Q(evaluador=self.request.user) |
                models.Q(asistente__evento__instructor=self.request.user)
            )
        return Evaluacion.objects.all()
