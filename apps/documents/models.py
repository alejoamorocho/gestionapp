from django.db import models
from django.conf import settings
from apps.equipment.models import Equipo
from django.utils.text import slugify
import uuid

# Create your models here.

class CategoriaDocumento(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    slug = models.SlugField(unique=True, blank=True)
    padre = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategorias')
    orden = models.IntegerField(default=0)
    icono = models.CharField(max_length=50, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Categoría de Documento'
        verbose_name_plural = 'Categorías de Documentos'
        ordering = ['orden', 'nombre']

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

class Documento(models.Model):
    TIPO_CHOICES = [
        ('MANUAL', 'Manual de Usuario'),
        ('FICHA_TECNICA', 'Ficha Técnica'),
        ('CERTIFICADO', 'Certificado'),
        ('GARANTIA', 'Garantía'),
        ('PROCEDIMIENTO', 'Procedimiento'),
        ('OTRO', 'Otro'),
    ]

    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    categoria = models.ForeignKey(CategoriaDocumento, on_delete=models.PROTECT, related_name='documentos')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    archivo = models.FileField(upload_to='documentos/')
    version = models.CharField(max_length=20)
    equipo = models.ForeignKey(
        Equipo, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='documentos_sistema'
    )
    publico = models.BooleanField(default=False, help_text='Si es público, será visible para todos los usuarios')
    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='documentos_creados'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    fecha_expiracion = models.DateTimeField(null=True, blank=True)
    tags = models.CharField(max_length=500, blank=True, help_text='Tags separados por comas')
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        verbose_name = 'Documento'
        verbose_name_plural = 'Documentos'
        ordering = ['-fecha_actualizacion']

    def __str__(self):
        return f"{self.titulo} - v{self.version}"

    @property
    def extension(self):
        return self.archivo.name.split('.')[-1].lower() if self.archivo else ''

class VersionDocumento(models.Model):
    documento = models.ForeignKey(Documento, on_delete=models.CASCADE, related_name='versiones')
    version = models.CharField(max_length=20)
    archivo = models.FileField(upload_to='documentos/versiones/')
    notas_cambios = models.TextField()
    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='versiones_documentos'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Versión de Documento'
        verbose_name_plural = 'Versiones de Documentos'
        ordering = ['-fecha_creacion']
        unique_together = ['documento', 'version']

    def __str__(self):
        return f"{self.documento.titulo} - v{self.version}"

class PermisoDocumento(models.Model):
    TIPO_PERMISO_CHOICES = [
        ('LECTURA', 'Lectura'),
        ('ESCRITURA', 'Escritura'),
        ('ADMINISTRACION', 'Administración'),
    ]

    documento = models.ForeignKey(Documento, on_delete=models.CASCADE, related_name='permisos')
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='permisos_documentos'
    )
    tipo_permiso = models.CharField(max_length=20, choices=TIPO_PERMISO_CHOICES)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_expiracion = models.DateTimeField(null=True, blank=True)
    otorgado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='permisos_otorgados'
    )

    class Meta:
        verbose_name = 'Permiso de Documento'
        verbose_name_plural = 'Permisos de Documentos'
        unique_together = ['documento', 'usuario']

    def __str__(self):
        return f"{self.usuario} - {self.documento} ({self.get_tipo_permiso_display()})"

class HistorialAcceso(models.Model):
    TIPO_ACCION_CHOICES = [
        ('VER', 'Ver'),
        ('DESCARGAR', 'Descargar'),
        ('EDITAR', 'Editar'),
        ('ELIMINAR', 'Eliminar'),
    ]

    documento = models.ForeignKey(Documento, on_delete=models.CASCADE, related_name='historial_accesos')
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='historial_accesos_documentos'
    )
    tipo_accion = models.CharField(max_length=20, choices=TIPO_ACCION_CHOICES)
    fecha_acceso = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    detalles = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Historial de Acceso'
        verbose_name_plural = 'Historial de Accesos'
        ordering = ['-fecha_acceso']

    def __str__(self):
        return f"{self.usuario} - {self.documento} - {self.get_tipo_accion_display()}"
