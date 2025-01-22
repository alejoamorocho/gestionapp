from django.db import models
from django.conf import settings

# Create your models here.

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    imagen = models.ImageField(upload_to='categorias/', blank=True, null=True)

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

class Fabricante(models.Model):
    nombre = models.CharField(max_length=100)
    pais = models.CharField(max_length=50)
    sitio_web = models.URLField(blank=True)
    contacto_nombre = models.CharField(max_length=100, blank=True)
    contacto_email = models.EmailField(blank=True)
    contacto_telefono = models.CharField(max_length=20, blank=True)
    notas = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Fabricante'
        verbose_name_plural = 'Fabricantes'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

class Equipo(models.Model):
    ESTADO_CHOICES = [
        ('DISPONIBLE', 'Disponible'),
        ('VENDIDO', 'Vendido'),
        ('MANTENIMIENTO', 'En Mantenimiento'),
        ('RESERVADO', 'Reservado'),
        ('DESCONTINUADO', 'Descontinuado'),
    ]

    # Información del modelo de equipo
    nombre = models.CharField(max_length=200)
    modelo = models.CharField(max_length=100)
    referencia = models.CharField(max_length=100, default='SIN-REF')
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    fabricante = models.ForeignKey(Fabricante, on_delete=models.PROTECT)
    descripcion = models.TextField()
    especificaciones_tecnicas = models.TextField()
    
    # Información específica de la unidad
    numero_serie = models.CharField(max_length=100, unique=True)
    cliente_asignado = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='equipos_asignados',
        limit_choices_to={'tipo': 'CLIENTE'}
    )
    ubicacion = models.CharField(max_length=200, blank=True)
    fecha_instalacion = models.DateField(null=True, blank=True)
    
    # Información comercial y técnica
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='DISPONIBLE')
    fecha_fabricacion = models.DateField()
    fecha_adquisicion = models.DateField()
    garantia_meses = models.IntegerField()
    requiere_capacitacion = models.BooleanField(default=False)
    capacitacion_realizada = models.BooleanField(default=False)
    fecha_ultima_capacitacion = models.DateField(null=True, blank=True)
    
    # Archivos y documentación
    notas = models.TextField(blank=True)
    imagen_principal = models.ImageField(upload_to='equipos/')
    manual_usuario = models.FileField(upload_to='manuales/', blank=True)
    certificaciones = models.TextField(blank=True)
    
    # Campos del sistema
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Equipo'
        verbose_name_plural = 'Equipos'
        ordering = ['-fecha_creacion']
        unique_together = ['referencia', 'numero_serie']

    def __str__(self):
        return f"{self.nombre} - {self.modelo} ({self.numero_serie})"

    def esta_en_garantia(self):
        from datetime import date
        meses_transcurridos = (date.today().year - self.fecha_adquisicion.year) * 12 + \
                             (date.today().month - self.fecha_adquisicion.month)
        return meses_transcurridos <= self.garantia_meses

class ImagenEquipo(models.Model):
    equipo = models.ForeignKey(Equipo, related_name='imagenes', on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='equipos/')
    descripcion = models.CharField(max_length=200, blank=True)
    es_principal = models.BooleanField(default=False)
    orden = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Imagen de Equipo'
        verbose_name_plural = 'Imágenes de Equipos'
        ordering = ['orden']

    def __str__(self):
        return f"Imagen {self.orden} de {self.equipo}"

class DocumentoEquipo(models.Model):
    TIPO_CHOICES = [
        ('MANUAL', 'Manual de Usuario'),
        ('CERTIFICADO', 'Certificado'),
        ('GARANTIA', 'Garantía'),
        ('SERVICIO', 'Historial de Servicio'),
        ('OTRO', 'Otro'),
    ]

    equipo = models.ForeignKey(Equipo, related_name='documentos', on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    titulo = models.CharField(max_length=200)
    archivo = models.FileField(upload_to='documentos/')
    descripcion = models.TextField(blank=True)
    fecha_subida = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Documento de Equipo'
        verbose_name_plural = 'Documentos de Equipos'
        ordering = ['-fecha_subida']

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.titulo}"

class HistorialPrecio(models.Model):
    equipo = models.ForeignKey(Equipo, related_name='historial_precios', on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    notas = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Historial de Precio'
        verbose_name_plural = 'Historial de Precios'
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.equipo} - ${self.precio} ({self.fecha.date()})"
