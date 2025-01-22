from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class Usuario(AbstractUser):
    TIPO_CHOICES = [
        ('ADMIN', 'Administrador'),
        ('CLIENTE', 'Cliente Profesional'),
        ('TECNICO', 'Técnico Especializado'),
        ('VENDEDOR', 'Vendedor'),
    ]
    
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    telefono = models.CharField(max_length=20)
    direccion = models.TextField(blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    especialidad = models.CharField(max_length=100, blank=True)
    numero_colegiatura = models.CharField(max_length=50, blank=True)
    certificaciones = models.TextField(blank=True)
    area_servicio = models.CharField(max_length=100, blank=True)
    notas = models.TextField(blank=True)
    imagen_perfil = models.ImageField(upload_to='perfiles/', null=True, blank=True)
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        
    def __str__(self):
        return f"{self.get_full_name()} - {self.get_tipo_display()}"
        
    def es_tecnico(self):
        return self.tipo == 'TECNICO'
        
    def es_cliente_profesional(self):
        return self.tipo == 'CLIENTE'
