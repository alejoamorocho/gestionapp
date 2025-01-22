from rest_framework import serializers
from .models import Categoria, Fabricante, Equipo, ImagenEquipo, DocumentoEquipo, HistorialPrecio

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class FabricanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fabricante
        fields = '__all__'

class ImagenEquipoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagenEquipo
        fields = '__all__'

class DocumentoEquipoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentoEquipo
        fields = '__all__'

class HistorialPrecioSerializer(serializers.ModelSerializer):
    usuario_nombre = serializers.CharField(source='usuario.get_full_name', read_only=True)

    class Meta:
        model = HistorialPrecio
        fields = '__all__'

class EquipoListSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)
    fabricante_nombre = serializers.CharField(source='fabricante.nombre', read_only=True)
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)
    cliente_nombre = serializers.CharField(source='cliente_asignado.get_full_name', read_only=True)

    class Meta:
        model = Equipo
        fields = ['id', 'nombre', 'modelo', 'referencia', 'numero_serie',
                 'categoria_nombre', 'fabricante_nombre', 'cliente_nombre',
                 'precio', 'estado', 'estado_display', 'ubicacion',
                 'capacitacion_realizada', 'imagen_principal']

class EquipoDetailSerializer(serializers.ModelSerializer):
    categoria = CategoriaSerializer(read_only=True)
    fabricante = FabricanteSerializer(read_only=True)
    imagenes = ImagenEquipoSerializer(many=True, read_only=True)
    documentos = DocumentoEquipoSerializer(many=True, read_only=True)
    historial_precios = HistorialPrecioSerializer(many=True, read_only=True)
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)
    en_garantia = serializers.BooleanField(source='esta_en_garantia', read_only=True)
    cliente_nombre = serializers.CharField(source='cliente_asignado.get_full_name', read_only=True)

    class Meta:
        model = Equipo
        fields = '__all__'

class EquipoCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipo
        fields = '__all__'
        read_only_fields = ('fecha_creacion', 'fecha_actualizacion')
        
    def validate(self, data):
        # Validar que la fecha de instalación sea posterior a la fecha de adquisición
        if data.get('fecha_instalacion') and data.get('fecha_adquisicion'):
            if data['fecha_instalacion'] < data['fecha_adquisicion']:
                raise serializers.ValidationError({
                    'fecha_instalacion': 'La fecha de instalación no puede ser anterior a la fecha de adquisición'
                })
        
        # Validar que la fecha de capacitación sea posterior a la fecha de instalación
        if data.get('fecha_ultima_capacitacion') and data.get('fecha_instalacion'):
            if data['fecha_ultima_capacitacion'] < data['fecha_instalacion']:
                raise serializers.ValidationError({
                    'fecha_ultima_capacitacion': 'La fecha de capacitación no puede ser anterior a la fecha de instalación'
                })
        
        # Si se marca como capacitación realizada, debe tener fecha de capacitación
        if data.get('capacitacion_realizada') and not data.get('fecha_ultima_capacitacion'):
            raise serializers.ValidationError({
                'fecha_ultima_capacitacion': 'Debe especificar la fecha de la última capacitación'
            })
        
        return data
