from django.db import models
from django.conf import settings
from apps.equipment.models import Equipo

class Evento(models.Model):
    TIPO_CHOICES = [
        ('CAPACITACION', 'Capacitación Técnica'),
        ('DEMOSTRACION', 'Demostración de Equipo'),
        ('CERTIFICACION', 'Certificación'),
        ('SEMINARIO', 'Seminario'),
        ('OTRO', 'Otro'),
    ]

    MODALIDAD_CHOICES = [
        ('PRESENCIAL', 'Presencial'),
        ('VIRTUAL', 'Virtual'),
        ('HIBRIDO', 'Híbrido'),
    ]

    titulo = models.CharField(max_length=200)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    descripcion = models.TextField()
    modalidad = models.CharField(max_length=20, choices=MODALIDAD_CHOICES)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    ubicacion = models.CharField(max_length=200, blank=True)
    link_virtual = models.URLField(blank=True)
    capacidad_maxima = models.IntegerField()
    equipos = models.ManyToManyField(Equipo, blank=True, related_name='eventos')
    instructor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='eventos_como_instructor',
        limit_choices_to={'tipo': 'TECNICO'}
    )
    requisitos = models.TextField(blank=True)
    materiales = models.TextField(blank=True)
    costo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    activo = models.BooleanField(default=True)
    notas = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'
        ordering = ['-fecha_inicio']

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.titulo}"

    @property
    def plazas_disponibles(self):
        return self.capacidad_maxima - self.asistentes.count()

    @property
    def esta_lleno(self):
        return self.plazas_disponibles <= 0

class Asistente(models.Model):
    ESTADO_CHOICES = [
        ('REGISTRADO', 'Registrado'),
        ('CONFIRMADO', 'Confirmado'),
        ('COMPLETADO', 'Completado'),
        ('CANCELADO', 'Cancelado'),
        ('NO_ASISTIO', 'No Asistió'),
    ]

    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='asistentes')
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='eventos_registrados'
    )
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='REGISTRADO')
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_confirmacion = models.DateTimeField(null=True, blank=True)
    asistio = models.BooleanField(default=False)
    calificacion = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    comentarios = models.TextField(blank=True)
    certificado_emitido = models.BooleanField(default=False)
    fecha_certificado = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Asistente'
        verbose_name_plural = 'Asistentes'
        ordering = ['evento', 'fecha_registro']
        unique_together = ['evento', 'usuario']

    def __str__(self):
        return f"{self.usuario.get_full_name()} - {self.evento}"

class MaterialEvento(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='materiales_adjuntos')
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    archivo = models.FileField(upload_to='eventos/materiales/')
    publico = models.BooleanField(default=False, help_text='Si es público, estará disponible antes del evento')
    orden = models.IntegerField(default=0)
    fecha_subida = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Material de Evento'
        verbose_name_plural = 'Materiales de Eventos'
        ordering = ['evento', 'orden', 'titulo']

    def __str__(self):
        return f"{self.titulo} - {self.evento}"

class Certificado(models.Model):
    asistente = models.OneToOneField(Asistente, on_delete=models.CASCADE, related_name='certificado')
    numero_certificado = models.CharField(max_length=100, unique=True)
    fecha_emision = models.DateTimeField(auto_now_add=True)
    archivo = models.FileField(upload_to='eventos/certificados/')
    firmado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='certificados_firmados'
    )
    notas = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Certificado'
        verbose_name_plural = 'Certificados'
        ordering = ['-fecha_emision']

    def __str__(self):
        return f"Certificado {self.numero_certificado} - {self.asistente}"

class Evaluacion(models.Model):
    asistente = models.OneToOneField(Asistente, on_delete=models.CASCADE, related_name='evaluacion')
    fecha_evaluacion = models.DateTimeField(auto_now_add=True)
    calificacion_teorica = models.DecimalField(max_digits=5, decimal_places=2)
    calificacion_practica = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    observaciones = models.TextField(blank=True)
    aprobado = models.BooleanField(default=False)
    evaluador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='evaluaciones_realizadas'
    )

    class Meta:
        verbose_name = 'Evaluación'
        verbose_name_plural = 'Evaluaciones'
        ordering = ['-fecha_evaluacion']

    def __str__(self):
        return f"Evaluación de {self.asistente}"

    @property
    def calificacion_final(self):
        if self.calificacion_practica:
            return (self.calificacion_teorica + self.calificacion_practica) / 2
        return self.calificacion_teorica
