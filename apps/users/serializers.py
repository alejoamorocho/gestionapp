from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

Usuario = get_user_model()

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 
                 'tipo', 'telefono', 'direccion', 'especialidad', 
                 'numero_colegiatura', 'certificaciones', 'area_servicio',
                 'notas', 'imagen_perfil')
        read_only_fields = ('id',)

class UsuarioCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Usuario
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name',
                 'tipo', 'telefono', 'direccion', 'especialidad', 
                 'numero_colegiatura', 'certificaciones', 'area_servicio',
                 'notas', 'imagen_perfil')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Las contraseñas no coinciden"})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = Usuario.objects.create_user(**validated_data)
        return user

class UsuarioUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('first_name', 'last_name', 'email', 'telefono', 
                 'direccion', 'especialidad', 'numero_colegiatura', 
                 'certificaciones', 'area_servicio', 'notas', 'imagen_perfil')
        
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
