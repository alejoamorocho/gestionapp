from django.shortcuts import render
from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.db.models import Q
from .models import (
    CategoriaDocumento, Documento, VersionDocumento,
    PermisoDocumento, HistorialAcceso
)
from .serializers import (
    CategoriaDocumentoSerializer, DocumentoListSerializer,
    DocumentoDetailSerializer, DocumentoCreateUpdateSerializer,
    VersionDocumentoSerializer, PermisoDocumentoSerializer,
    PermisoDocumentoCreateSerializer, HistorialAccesoSerializer
)

# Create your views here.

class CategoriaDocumentoViewSet(viewsets.ModelViewSet):
    queryset = CategoriaDocumento.objects.all()
    serializer_class = CategoriaDocumentoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre', 'descripcion']
    ordering_fields = ['orden', 'nombre']

class DocumentoViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['categoria', 'tipo', 'equipo', 'publico']
    search_fields = ['titulo', 'descripcion', 'tags']
    ordering_fields = ['fecha_actualizacion', 'titulo', 'version']

    def get_queryset(self):
        user = self.request.user
        # Administradores ven todo
        if user.is_staff:
            return Documento.objects.all()
        
        # Otros usuarios ven documentos públicos y aquellos a los que tienen permiso
        return Documento.objects.filter(
            Q(publico=True) |
            Q(permisos__usuario=user) |
            Q(creado_por=user)
        ).distinct()

    def get_serializer_class(self):
        if self.action == 'list':
            return DocumentoListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return DocumentoCreateUpdateSerializer
        return DocumentoDetailSerializer

    def perform_create(self, serializer):
        serializer.save(creado_por=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Registrar el acceso
        HistorialAcceso.objects.create(
            documento=instance,
            usuario=request.user,
            tipo_accion='VER',
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def nueva_version(self, request, pk=None):
        documento = self.get_object()
        serializer = VersionDocumentoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                documento=documento,
                creado_por=request.user
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def asignar_permiso(self, request, pk=None):
        documento = self.get_object()
        serializer = PermisoDocumentoCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                documento=documento,
                otorgado_por=request.user
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VersionDocumentoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = VersionDocumento.objects.all()
    serializer_class = VersionDocumentoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['documento']
    ordering_fields = ['fecha_creacion', 'version']

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return VersionDocumento.objects.all()
        return VersionDocumento.objects.filter(
            Q(documento__publico=True) |
            Q(documento__permisos__usuario=user) |
            Q(documento__creado_por=user)
        ).distinct()

class PermisoDocumentoViewSet(viewsets.ModelViewSet):
    queryset = PermisoDocumento.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['documento', 'usuario', 'tipo_permiso']
    ordering_fields = ['fecha_creacion']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return PermisoDocumentoCreateSerializer
        return PermisoDocumentoSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return PermisoDocumento.objects.all()
        return PermisoDocumento.objects.filter(
            Q(usuario=user) |
            Q(documento__creado_por=user)
        ).distinct()

class HistorialAccesoViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = HistorialAccesoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['documento', 'usuario', 'tipo_accion']
    ordering_fields = ['fecha_acceso']

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return HistorialAcceso.objects.all()
        return HistorialAcceso.objects.filter(
            Q(usuario=user) |
            Q(documento__creado_por=user)
        ).distinct()
