from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'tipo', 'especialidad', 'is_staff')
    list_filter = ('tipo', 'especialidad', 'is_staff', 'is_superuser', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Información Personal', {
            'fields': ('first_name', 'last_name', 'email', 'telefono', 
                      'direccion', 'imagen_perfil')
        }),
        ('Información Profesional', {
            'fields': ('especialidad', 'numero_colegiatura', 'certificaciones', 
                      'area_servicio', 'notas')
        }),
        ('Permisos', {
            'fields': ('tipo', 'is_active', 'is_staff', 'is_superuser', 
                      'groups', 'user_permissions')
        }),
        ('Fechas Importantes', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'tipo', 
                      'especialidad', 'numero_colegiatura'),
        }),
    )
    search_fields = ('username', 'first_name', 'last_name', 'email', 
                    'especialidad', 'numero_colegiatura')
    ordering = ('username',)

admin.site.register(Usuario, CustomUserAdmin)
