from django.contrib import admin
from .models import (
    CategoriaDocumento, Documento, VersionDocumento,
    PermisoDocumento, HistorialAcceso
)

@admin.register(CategoriaDocumento)
class CategoriaDocumentoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'padre', 'orden', 'fecha_actualizacion']
    list_filter = ['padre']
    search_fields = ['nombre', 'descripcion']
    prepopulated_fields = {'slug': ('nombre',)}
    ordering = ['orden', 'nombre']

class VersionDocumentoInline(admin.TabularInline):
    model = VersionDocumento
    extra = 0
    readonly_fields = ['fecha_creacion']

class PermisoDocumentoInline(admin.TabularInline):
    model = PermisoDocumento
    extra = 0
    readonly_fields = ['fecha_creacion']

@admin.register(Documento)
class DocumentoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'tipo', 'categoria', 'version', 'publico', 'creado_por', 'fecha_actualizacion']
    list_filter = ['tipo', 'categoria', 'publico', 'creado_por']
    search_fields = ['titulo', 'descripcion', 'tags']
    readonly_fields = ['uuid', 'fecha_creacion', 'fecha_actualizacion']
    inlines = [VersionDocumentoInline, PermisoDocumentoInline]
    date_hierarchy = 'fecha_creacion'

    def save_model(self, request, obj, form, change):
        if not change:  # Si es una nueva instancia
            obj.creado_por = request.user
        super().save_model(request, obj, form, change)

@admin.register(VersionDocumento)
class VersionDocumentoAdmin(admin.ModelAdmin):
    list_display = ['documento', 'version', 'creado_por', 'fecha_creacion']
    list_filter = ['creado_por', 'fecha_creacion']
    search_fields = ['documento__titulo', 'version', 'notas_cambios']
    readonly_fields = ['fecha_creacion']

@admin.register(PermisoDocumento)
class PermisoDocumentoAdmin(admin.ModelAdmin):
    list_display = ['documento', 'usuario', 'tipo_permiso', 'fecha_creacion', 'fecha_expiracion']
    list_filter = ['tipo_permiso', 'fecha_creacion', 'fecha_expiracion']
    search_fields = ['documento__titulo', 'usuario__email']
    readonly_fields = ['fecha_creacion']

@admin.register(HistorialAcceso)
class HistorialAccesoAdmin(admin.ModelAdmin):
    list_display = ['documento', 'usuario', 'tipo_accion', 'fecha_acceso', 'ip_address']
    list_filter = ['tipo_accion', 'fecha_acceso']
    search_fields = ['documento__titulo', 'usuario__email', 'ip_address']
    readonly_fields = ['fecha_acceso']
    date_hierarchy = 'fecha_acceso'
