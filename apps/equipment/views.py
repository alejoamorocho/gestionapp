from django.shortcuts import render
from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Categoria, Fabricante, Equipo, ImagenEquipo, DocumentoEquipo, HistorialPrecio
from .serializers import (
    CategoriaSerializer, FabricanteSerializer,
    EquipoListSerializer, EquipoDetailSerializer, EquipoCreateUpdateSerializer,
    ImagenEquipoSerializer, DocumentoEquipoSerializer, HistorialPrecioSerializer
)

# Create your views here.

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre', 'descripcion']
    ordering_fields = ['nombre']

class FabricanteViewSet(viewsets.ModelViewSet):
    queryset = Fabricante.objects.all()
    serializer_class = FabricanteSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre', 'pais', 'contacto_nombre']
    ordering_fields = ['nombre', 'pais']

class EquipoViewSet(viewsets.ModelViewSet):
    queryset = Equipo.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['categoria', 'fabricante', 'estado', 'requiere_capacitacion']
    search_fields = ['nombre', 'modelo', 'numero_serie', 'descripcion']
    ordering_fields = ['nombre', 'precio', 'fecha_creacion', 'fecha_actualizacion']

    def get_serializer_class(self):
        if self.action == 'list':
            return EquipoListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return EquipoCreateUpdateSerializer
        return EquipoDetailSerializer

class ImagenEquipoViewSet(viewsets.ModelViewSet):
    queryset = ImagenEquipo.objects.all()
    serializer_class = ImagenEquipoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['equipo', 'es_principal']
    ordering_fields = ['orden']

class DocumentoEquipoViewSet(viewsets.ModelViewSet):
    queryset = DocumentoEquipo.objects.all()
    serializer_class = DocumentoEquipoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['equipo', 'tipo']
    search_fields = ['titulo', 'descripcion']
    ordering_fields = ['fecha_subida']

class HistorialPrecioViewSet(viewsets.ModelViewSet):
    queryset = HistorialPrecio.objects.all()
    serializer_class = HistorialPrecioSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['equipo']
    ordering_fields = ['fecha']

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)
