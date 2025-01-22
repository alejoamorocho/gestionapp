from rest_framework import serializers
from .models import Evento, Asistente, MaterialEvento, Certificado, Evaluacion
from apps.users.serializers import UsuarioSerializer
from apps.equipment.serializers import EquipoListSerializer

class MaterialEventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialEvento
        fields = '__all__'

class CertificadoSerializer(serializers.ModelSerializer):
    firmado_por = UsuarioSerializer(read_only=True)

    class Meta:
        model = Certificado
        fields = '__all__'

class EvaluacionSerializer(serializers.ModelSerializer):
    evaluador = UsuarioSerializer(read_only=True)
    calificacion_final = serializers.DecimalField(max_digits=5, decimal_places=2, read_only=True)

    class Meta:
        model = Evaluacion
        fields = '__all__'

class AsistenteListSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer(read_only=True)
    
    class Meta:
        model = Asistente
        fields = ['id', 'usuario', 'estado', 'asistio', 'certificado_emitido']

class AsistenteDetailSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer(read_only=True)
    certificado = CertificadoSerializer(read_only=True)
    evaluacion = EvaluacionSerializer(read_only=True)
    
    class Meta:
        model = Asistente
        fields = '__all__'

class EventoListSerializer(serializers.ModelSerializer):
    instructor = UsuarioSerializer(read_only=True)
    plazas_disponibles = serializers.IntegerField(read_only=True)
    esta_lleno = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Evento
        fields = [
            'id', 'titulo', 'tipo', 'modalidad', 'fecha_inicio', 'fecha_fin',
            'instructor', 'capacidad_maxima', 'plazas_disponibles', 'esta_lleno',
            'activo'
        ]

class EventoDetailSerializer(serializers.ModelSerializer):
    instructor = UsuarioSerializer(read_only=True)
    equipos = EquipoListSerializer(many=True, read_only=True)
    asistentes = AsistenteListSerializer(many=True, read_only=True)
    materiales_adjuntos = MaterialEventoSerializer(many=True, read_only=True)
    plazas_disponibles = serializers.IntegerField(read_only=True)
    esta_lleno = serializers.BooleanField(read_only=True)

    class Meta:
        model = Evento
        fields = '__all__'

class EventoCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evento
        fields = '__all__'
        read_only_fields = ['fecha_creacion', 'fecha_actualizacion']

    def validate(self, data):
        if data['fecha_fin'] <= data['fecha_inicio']:
            raise serializers.ValidationError(
                "La fecha de finalización debe ser posterior a la fecha de inicio"
            )
        return data

class AsistenteCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asistente
        fields = '__all__'
        read_only_fields = ['fecha_registro', 'fecha_certificado']

    def validate(self, data):
        # Verificar si hay plazas disponibles
        evento = data['evento']
        if evento.esta_lleno and data['estado'] != 'CANCELADO':
            raise serializers.ValidationError(
                "No hay plazas disponibles para este evento"
            )
        return data
