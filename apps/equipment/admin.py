from django.contrib import admin
from .models import Categoria, Fabricante, Equipo, ImagenEquipo, DocumentoEquipo, HistorialPrecio

# Register your models here.

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre', 'descripcion')

@admin.register(Fabricante)
class FabricanteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'pais', 'contacto_nombre', 'contacto_email')
    search_fields = ('nombre', 'pais', 'contacto_nombre')
    list_filter = ('pais',)

class ImagenEquipoInline(admin.TabularInline):
    model = ImagenEquipo
    extra = 1

class DocumentoEquipoInline(admin.TabularInline):
    model = DocumentoEquipo
    extra = 1

class HistorialPrecioInline(admin.TabularInline):
    model = HistorialPrecio
    extra = 0
    readonly_fields = ('fecha', 'usuario')
    can_delete = False

@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'modelo', 'referencia', 'numero_serie', 'cliente_asignado',
                   'estado', 'esta_en_garantia', 'capacitacion_realizada')
    list_filter = ('categoria', 'fabricante', 'estado', 'requiere_capacitacion',
                  'capacitacion_realizada')
    search_fields = ('nombre', 'modelo', 'referencia', 'numero_serie', 'descripcion',
                    'cliente_asignado__first_name', 'cliente_asignado__last_name')
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion')
    inlines = [ImagenEquipoInline, DocumentoEquipoInline, HistorialPrecioInline]
    fieldsets = (
        ('Información del Modelo', {
            'fields': ('nombre', 'modelo', 'referencia', 'categoria', 'fabricante', 'descripcion')
        }),
        ('Información de la Unidad', {
            'fields': ('numero_serie', 'cliente_asignado', 'ubicacion', 'fecha_instalacion')
        }),
        ('Especificaciones', {
            'fields': ('especificaciones_tecnicas', 'certificaciones')
        }),
        ('Información Comercial', {
            'fields': ('precio', 'estado')
        }),
        ('Capacitación', {
            'fields': ('requiere_capacitacion', 'capacitacion_realizada', 'fecha_ultima_capacitacion')
        }),
        ('Fechas', {
            'fields': ('fecha_fabricacion', 'fecha_adquisicion', 'garantia_meses')
        }),
        ('Archivos', {
            'fields': ('imagen_principal', 'manual_usuario')
        }),
        ('Notas y Fechas del Sistema', {
            'fields': ('notas', 'fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:  # Si es una creación nueva
            obj.save()
            # Crear el primer registro en el historial de precios
            HistorialPrecio.objects.create(
                equipo=obj,
                precio=obj.precio,
                usuario=request.user,
                notas='Precio inicial del equipo'
            )
        else:  # Si es una actualización
            if 'precio' in form.changed_data:
                # Si el precio cambió, crear un nuevo registro en el historial
                HistorialPrecio.objects.create(
                    equipo=obj,
                    precio=obj.precio,
                    usuario=request.user,
                    notas='Actualización de precio'
                )
            obj.save()

@admin.register(ImagenEquipo)
class ImagenEquipoAdmin(admin.ModelAdmin):
    list_display = ('equipo', 'descripcion', 'es_principal', 'orden')
    list_filter = ('equipo', 'es_principal')
    search_fields = ('equipo__nombre', 'descripcion')

@admin.register(DocumentoEquipo)
class DocumentoEquipoAdmin(admin.ModelAdmin):
    list_display = ('equipo', 'tipo', 'titulo', 'fecha_subida')
    list_filter = ('tipo', 'fecha_subida')
    search_fields = ('equipo__nombre', 'titulo', 'descripcion')
    readonly_fields = ('fecha_subida',)

@admin.register(HistorialPrecio)
class HistorialPrecioAdmin(admin.ModelAdmin):
    list_display = ('equipo', 'precio', 'fecha', 'usuario')
    list_filter = ('fecha', 'usuario')
    search_fields = ('equipo__nombre', 'notas')
    readonly_fields = ('fecha', 'usuario')
    ordering = ('-fecha',)
