from django.db import models
from django.conf import settings
from apps.equipment.models import Equipo

class PlanMantenimiento(models.Model):
    FRECUENCIA_CHOICES = [
        ('SEMANAL', 'Semanal'),
        ('QUINCENAL', 'Quincenal'),
        ('MENSUAL', 'Mensual'),
        ('BIMESTRAL', 'Bimestral'),
        ('TRIMESTRAL', 'Trimestral'),
        ('SEMESTRAL', 'Semestral'),
        ('ANUAL', 'Anual'),
    ]

    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name='planes_mantenimiento')
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    frecuencia = models.CharField(max_length=20, choices=FRECUENCIA_CHOICES)
    duracion_estimada = models.DurationField(help_text='Duración estimada del mantenimiento')
    procedimiento = models.TextField(help_text='Procedimiento detallado del mantenimiento')
    herramientas_requeridas = models.TextField(blank=True)
    materiales_requeridos = models.TextField(blank=True)
    requiere_tecnico_especializado = models.BooleanField(default=False)
    notas = models.TextField(blank=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Plan de Mantenimiento'
        verbose_name_plural = 'Planes de Mantenimiento'
        ordering = ['equipo', 'frecuencia']

    def __str__(self):
        return f"{self.nombre} - {self.equipo} ({self.get_frecuencia_display()})"

class Mantenimiento(models.Model):
    ESTADO_CHOICES = [
        ('PROGRAMADO', 'Programado'),
        ('EN_PROCESO', 'En Proceso'),
        ('COMPLETADO', 'Completado'),
        ('CANCELADO', 'Cancelado'),
        ('REPROGRAMADO', 'Reprogramado'),
    ]

    TIPO_CHOICES = [
        ('PREVENTIVO', 'Preventivo'),
        ('CORRECTIVO', 'Correctivo'),
        ('PREDICTIVO', 'Predictivo'),
        ('INSTALACION', 'Instalación'),
        ('CALIBRACION', 'Calibración'),
    ]

    plan = models.ForeignKey(PlanMantenimiento, on_delete=models.SET_NULL, null=True, blank=True,
                            related_name='mantenimientos')
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name='mantenimientos')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='PROGRAMADO')
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha_programada = models.DateTimeField()
    fecha_inicio = models.DateTimeField(null=True, blank=True)
    fecha_fin = models.DateTimeField(null=True, blank=True)
    tecnico_asignado = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='mantenimientos_asignados',
        limit_choices_to={'tipo': 'TECNICO'}
    )
    costo_materiales = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    costo_mano_obra = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    diagnostico = models.TextField(blank=True)
    trabajo_realizado = models.TextField(blank=True)
    recomendaciones = models.TextField(blank=True)
    requiere_seguimiento = models.BooleanField(default=False)
    fecha_proximo_mantenimiento = models.DateField(null=True, blank=True)
    notas = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Mantenimiento'
        verbose_name_plural = 'Mantenimientos'
        ordering = ['-fecha_programada']

    def __str__(self):
        return f"{self.titulo} - {self.equipo} ({self.get_estado_display()})"

    @property
    def costo_total(self):
        return self.costo_materiales + self.costo_mano_obra

class FotoMantenimiento(models.Model):
    mantenimiento = models.ForeignKey(Mantenimiento, on_delete=models.CASCADE, related_name='fotos')
    imagen = models.ImageField(upload_to='mantenimientos/')
    descripcion = models.CharField(max_length=200)
    tipo = models.CharField(max_length=50, choices=[
        ('ANTES', 'Antes del mantenimiento'),
        ('DURANTE', 'Durante el mantenimiento'),
        ('DESPUES', 'Después del mantenimiento'),
        ('PROBLEMA', 'Problema encontrado'),
        ('OTRO', 'Otro'),
    ])
    fecha_subida = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Foto de Mantenimiento'
        verbose_name_plural = 'Fotos de Mantenimiento'
        ordering = ['mantenimiento', 'fecha_subida']

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.mantenimiento}"

class RepuestoUsado(models.Model):
    mantenimiento = models.ForeignKey(Mantenimiento, on_delete=models.CASCADE, related_name='repuestos')
    nombre = models.CharField(max_length=200)
    numero_parte = models.CharField(max_length=100)
    cantidad = models.IntegerField()
    costo_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    proveedor = models.CharField(max_length=200, blank=True)
    notas = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Repuesto Usado'
        verbose_name_plural = 'Repuestos Usados'
        ordering = ['mantenimiento', 'nombre']

    def __str__(self):
        return f"{self.nombre} ({self.numero_parte}) - {self.mantenimiento}"

    @property
    def costo_total(self):
        return self.cantidad * self.costo_unitario
