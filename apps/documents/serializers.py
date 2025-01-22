from rest_framework import serializers
from .models import (
    CategoriaDocumento, Documento, VersionDocumento,
    PermisoDocumento, HistorialAcceso
)
from apps.users.serializers import UsuarioSerializer
from apps.equipment.serializers import EquipoListSerializer

class CategoriaDocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaDocumento
        fields = '__all__'

class VersionDocumentoSerializer(serializers.ModelSerializer):
    creado_por = UsuarioSerializer(read_only=True)

    class Meta:
        model = VersionDocumento
        fields = '__all__'

class PermisoDocumentoSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer(read_only=True)
    otorgado_por = UsuarioSerializer(read_only=True)

    class Meta:
        model = PermisoDocumento
        fields = '__all__'

class HistorialAccesoSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer(read_only=True)

    class Meta:
        model = HistorialAcceso
        fields = '__all__'

class DocumentoListSerializer(serializers.ModelSerializer):
    categoria = CategoriaDocumentoSerializer(read_only=True)
    creado_por = UsuarioSerializer(read_only=True)
    extension = serializers.CharField(read_only=True)

    class Meta:
        model = Documento
        fields = [
            'id', 'titulo', 'tipo', 'version', 'categoria',
            'creado_por', 'fecha_actualizacion', 'extension',
            'publico', 'uuid'
        ]

class DocumentoDetailSerializer(serializers.ModelSerializer):
    categoria = CategoriaDocumentoSerializer(read_only=True)
    equipo = EquipoListSerializer(read_only=True)
    creado_por = UsuarioSerializer(read_only=True)
    versiones = VersionDocumentoSerializer(many=True, read_only=True)
    permisos = PermisoDocumentoSerializer(many=True, read_only=True)
    extension = serializers.CharField(read_only=True)

    class Meta:
        model = Documento
        fields = '__all__'

class DocumentoCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documento
        fields = '__all__'
        read_only_fields = ['uuid', 'fecha_creacion', 'fecha_actualizacion']

    def validate(self, data):
        # Validar el formato de versión (ejemplo: 1.0.0)
        version = data.get('version')
        if version:
            try:
                # Verificar que la versión tenga el formato correcto
                parts = version.split('.')
                if not all(part.isdigit() for part in parts):
                    raise serializers.ValidationError({
                        'version': 'La versión debe tener un formato válido (ejemplo: 1.0.0)'
                    })
            except:
                raise serializers.ValidationError({
                    'version': 'La versión debe tener un formato válido (ejemplo: 1.0.0)'
                })

        # Validar fechas de expiración
        fecha_expiracion = data.get('fecha_expiracion')
        if fecha_expiracion and fecha_expiracion < timezone.now():
            raise serializers.ValidationError({
                'fecha_expiracion': 'La fecha de expiración no puede ser anterior a la fecha actual'
            })

        return data

class PermisoDocumentoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermisoDocumento
        fields = '__all__'
        read_only_fields = ['fecha_creacion']

    def validate(self, data):
        # Verificar que el usuario no tenga ya un permiso para este documento
        if PermisoDocumento.objects.filter(
            documento=data['documento'],
            usuario=data['usuario']
        ).exists():
            raise serializers.ValidationError(
                'Este usuario ya tiene permisos asignados para este documento'
            )

        # Verificar fecha de expiración
        fecha_expiracion = data.get('fecha_expiracion')
        if fecha_expiracion and fecha_expiracion < timezone.now():
            raise serializers.ValidationError({
                'fecha_expiracion': 'La fecha de expiración no puede ser anterior a la fecha actual'
            })

        return data
