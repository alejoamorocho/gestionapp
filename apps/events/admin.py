from django.contrib import admin
from .models import Evento, Asistente, MaterialEvento, Certificado, Evaluacion

class MaterialEventoInline(admin.TabularInline):
    model = MaterialEvento
    extra = 1

class AsistenteInline(admin.TabularInline):
    model = Asistente
    extra = 0
    readonly_fields = ('fecha_registro', 'fecha_certificado')
    show_change_link = True

@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tipo', 'modalidad', 'fecha_inicio', 'fecha_fin',
                   'instructor', 'capacidad_maxima', 'plazas_disponibles', 'activo')
    list_filter = ('tipo', 'modalidad', 'activo', 'instructor')
    search_fields = ('titulo', 'descripcion', 'ubicacion')
    inlines = [MaterialEventoInline, AsistenteInline]
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion', 'plazas_disponibles')
    fieldsets = (
        ('Información Básica', {
            'fields': ('titulo', 'tipo', 'descripcion', 'modalidad')
        }),
        ('Programación', {
            'fields': ('fecha_inicio', 'fecha_fin', 'ubicacion', 'link_virtual')
        }),
        ('Capacidad y Equipos', {
            'fields': ('capacidad_maxima', 'plazas_disponibles', 'equipos')
        }),
        ('Instructor y Requisitos', {
            'fields': ('instructor', 'requisitos', 'materiales')
        }),
        ('Costos y Estado', {
            'fields': ('costo', 'activo')
        }),
        ('Notas y Fechas del Sistema', {
            'fields': ('notas', 'fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        })
    )

@admin.register(Asistente)
class AsistenteAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'evento', 'estado', 'asistio',
                   'certificado_emitido', 'fecha_registro')
    list_filter = ('estado', 'asistio', 'certificado_emitido', 'evento')
    search_fields = ('usuario__email', 'usuario__first_name', 'usuario__last_name')
    readonly_fields = ('fecha_registro', 'fecha_certificado')
    raw_id_fields = ('usuario', 'evento')

@admin.register(MaterialEvento)
class MaterialEventoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'evento', 'publico', 'orden', 'fecha_subida')
    list_filter = ('publico', 'evento')
    search_fields = ('titulo', 'descripcion')
    ordering = ('evento', 'orden', 'titulo')

@admin.register(Certificado)
class CertificadoAdmin(admin.ModelAdmin):
    list_display = ('numero_certificado', 'asistente', 'fecha_emision', 'firmado_por')
    list_filter = ('fecha_emision', 'firmado_por')
    search_fields = ('numero_certificado', 'asistente__usuario__email')
    raw_id_fields = ('asistente',)
    readonly_fields = ('fecha_emision',)

@admin.register(Evaluacion)
class EvaluacionAdmin(admin.ModelAdmin):
    list_display = ('asistente', 'calificacion_teorica', 'calificacion_practica',
                   'calificacion_final', 'aprobado', 'fecha_evaluacion')
    list_filter = ('aprobado', 'fecha_evaluacion', 'evaluador')
    search_fields = ('asistente__usuario__email', 'observaciones')
    raw_id_fields = ('asistente',)
    readonly_fields = ('fecha_evaluacion',)
