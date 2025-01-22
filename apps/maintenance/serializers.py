from rest_framework import serializers
from .models import PlanMantenimiento, Mantenimiento, FotoMantenimiento, RepuestoUsado

class FotoMantenimientoSerializer(serializers.ModelSerializer):
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)

    class Meta:
        model = FotoMantenimiento
        fields = '__all__'

class RepuestoUsadoSerializer(serializers.ModelSerializer):
    costo_total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = RepuestoUsado
        fields = '__all__'

class PlanMantenimientoSerializer(serializers.ModelSerializer):
    frecuencia_display = serializers.CharField(source='get_frecuencia_display', read_only=True)

    class Meta:
        model = PlanMantenimiento
        fields = '__all__'

class MantenimientoListSerializer(serializers.ModelSerializer):
    equipo_nombre = serializers.CharField(source='equipo.nombre', read_only=True)
    tecnico_nombre = serializers.CharField(source='tecnico_asignado.get_full_name', read_only=True)
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)

    class Meta:
        model = Mantenimiento
        fields = ['id', 'equipo', 'equipo_nombre', 'tipo', 'tipo_display',
                 'estado', 'estado_display', 'titulo', 'fecha_programada',
                 'tecnico_asignado', 'tecnico_nombre']

class MantenimientoDetailSerializer(serializers.ModelSerializer):
    equipo_nombre = serializers.CharField(source='equipo.nombre', read_only=True)
    tecnico_nombre = serializers.CharField(source='tecnico_asignado.get_full_name', read_only=True)
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    fotos = FotoMantenimientoSerializer(many=True, read_only=True)
    repuestos = RepuestoUsadoSerializer(many=True, read_only=True)
    costo_total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    plan_nombre = serializers.CharField(source='plan.nombre', read_only=True)

    class Meta:
        model = Mantenimiento
        fields = '__all__'

class MantenimientoCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mantenimiento
        fields = '__all__'
        read_only_fields = ('fecha_creacion', 'fecha_actualizacion')

    def validate(self, data):
        # Validar que la fecha de inicio sea anterior a la fecha de fin
        if data.get('fecha_inicio') and data.get('fecha_fin'):
            if data['fecha_inicio'] > data['fecha_fin']:
                raise serializers.ValidationError({
                    'fecha_fin': 'La fecha de fin debe ser posterior a la fecha de inicio'
                })

        # Validar que la fecha programada no sea anterior a la fecha actual
        from django.utils import timezone
        if data.get('fecha_programada') and data['fecha_programada'] < timezone.now():
            raise serializers.ValidationError({
                'fecha_programada': 'La fecha programada no puede ser anterior a la fecha actual'
            })

        # Si el estado es COMPLETADO, validar que tenga fecha de inicio y fin
        if data.get('estado') == 'COMPLETADO':
            if not data.get('fecha_inicio') or not data.get('fecha_fin'):
                raise serializers.ValidationError({
                    'estado': 'Un mantenimiento completado debe tener fecha de inicio y fin'
                })
            if not data.get('trabajo_realizado'):
                raise serializers.ValidationError({
                    'trabajo_realizado': 'Debe especificar el trabajo realizado para completar el mantenimiento'
                })

        # Si requiere seguimiento, debe tener fecha del próximo mantenimiento
        if data.get('requiere_seguimiento') and not data.get('fecha_proximo_mantenimiento'):
            raise serializers.ValidationError({
                'fecha_proximo_mantenimiento': 'Debe especificar la fecha del próximo mantenimiento'
            })

        return data
