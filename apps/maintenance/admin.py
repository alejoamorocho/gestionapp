from django.contrib import admin
from .models import PlanMantenimiento, Mantenimiento, FotoMantenimiento, RepuestoUsado

class FotoMantenimientoInline(admin.TabularInline):
    model = FotoMantenimiento
    extra = 1

class RepuestoUsadoInline(admin.TabularInline):
    model = RepuestoUsado
    extra = 1

@admin.register(PlanMantenimiento)
class PlanMantenimientoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'equipo', 'frecuencia', 'duracion_estimada',
                   'requiere_tecnico_especializado', 'activo')
    list_filter = ('frecuencia', 'requiere_tecnico_especializado', 'activo')
    search_fields = ('nombre', 'descripcion', 'procedimiento')
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'equipo', 'descripcion')
        }),
        ('Programación', {
            'fields': ('frecuencia', 'duracion_estimada')
        }),
        ('Requerimientos', {
            'fields': ('procedimiento', 'herramientas_requeridas', 'materiales_requeridos',
                      'requiere_tecnico_especializado')
        }),
        ('Estado y Notas', {
            'fields': ('activo', 'notas')
        })
    )

@admin.register(Mantenimiento)
class MantenimientoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'equipo', 'tipo', 'estado', 'fecha_programada',
                   'tecnico_asignado', 'costo_total')
    list_filter = ('tipo', 'estado', 'requiere_seguimiento')
    search_fields = ('titulo', 'descripcion', 'diagnostico', 'trabajo_realizado')
    inlines = [FotoMantenimientoInline, RepuestoUsadoInline]
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion', 'costo_total')
    fieldsets = (
        ('Información Básica', {
            'fields': ('plan', 'equipo', 'tipo', 'estado', 'titulo', 'descripcion')
        }),
        ('Programación', {
            'fields': ('fecha_programada', 'fecha_inicio', 'fecha_fin', 'tecnico_asignado')
        }),
        ('Costos', {
            'fields': ('costo_materiales', 'costo_mano_obra', 'costo_total')
        }),
        ('Detalles del Trabajo', {
            'fields': ('diagnostico', 'trabajo_realizado', 'recomendaciones')
        }),
        ('Seguimiento', {
            'fields': ('requiere_seguimiento', 'fecha_proximo_mantenimiento')
        }),
        ('Notas y Fechas del Sistema', {
            'fields': ('notas', 'fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        })
    )

    def costo_total(self, obj):
        return obj.costo_total
    costo_total.short_description = 'Costo Total'

@admin.register(FotoMantenimiento)
class FotoMantenimientoAdmin(admin.ModelAdmin):
    list_display = ('mantenimiento', 'tipo', 'descripcion', 'fecha_subida')
    list_filter = ('tipo', 'fecha_subida')
    search_fields = ('descripcion', 'mantenimiento__titulo')

@admin.register(RepuestoUsado)
class RepuestoUsadoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'numero_parte', 'mantenimiento', 'cantidad',
                   'costo_unitario', 'costo_total')
    list_filter = ('mantenimiento',)
    search_fields = ('nombre', 'numero_parte', 'proveedor')
    readonly_fields = ('costo_total',)

    def costo_total(self, obj):
        return obj.costo_total
    costo_total.short_description = 'Costo Total'
