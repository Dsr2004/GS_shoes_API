from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from .models import Usuario


class UsuarioSerializer(serializers.ModelSerializer):
    perfil = serializers.SerializerMethodField()
    class Meta:
        model = Usuario
        fields = [
            'id', 'correo', 'nombre_completo', 'identificacion', 'telefono', 'is_active', 'password', 'es_admin', 'perfil', 'created_at','updated_at'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'es_admin': {'write_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True}
        }

    def __init__(self, *args, **kwargs):
        super(UsuarioSerializer, self).__init__(*args, **kwargs)
        if self.instance is not None:
            self.fields['password'].required = False
            
    def get_perfil(self, obj):
        return 1 if obj.es_admin else 2

    def create(self, validated_data):
        es_admin = validated_data.pop('es_admin', False)
        password = validated_data.pop('password', None)

        if es_admin:
            usuario = Usuario.objects.create_superuser(
                correo=validated_data['correo'],
                nombre_completo=validated_data['nombre_completo'],
                identificacion=validated_data['identificacion'],
                telefono=validated_data['telefono'],
                password=password
            )
        else:
            usuario = Usuario.objects.create_user(
                correo=validated_data['correo'],
                nombre_completo=validated_data['nombre_completo'],
                identificacion=validated_data['identificacion'],
                telefono=validated_data['telefono'],
                password=password
            )
        return usuario

    def update(self, instance, validated_data):
        instance.correo = validated_data.get('correo', instance.correo)
        instance.nombre_completo = validated_data.get('nombre_completo', instance.nombre_completo)
        instance.identificacion = validated_data.get('identificacion', instance.identificacion)
        instance.telefono = validated_data.get('telefono', instance.telefono)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.es_admin = validated_data.get('es_admin', instance.es_admin)
        instance.is_superuser = instance.es_admin

        if 'password' in validated_data:
            instance.set_password(validated_data['password'])

        instance.save()
        return instance


class UsuarioLoginSerializer(serializers.Serializer):
    correo = serializers.EmailField()
    password = serializers.CharField(max_length=100)

    def validate(self, data):
        correo = data.get('correo')
        password = data.get('password')

        if not correo or not password:
            raise serializers.ValidationError({"error": "Debe proporcionar correo y contraseña."})

        try:
            usuario = Usuario.objects.get(correo=correo)
        except Usuario.DoesNotExist:
            raise serializers.ValidationError({"error": "Usuario no encontrado."})

        if not usuario.check_password(password):
            raise serializers.ValidationError({"error": "Contraseña incorrecta."})

        if not usuario.is_active:
            raise serializers.ValidationError({"error": "Cuenta inactiva. Contacte al administrador."})

        data['usuario'] = usuario
        return data


class PasswordResetRequestSerializer(serializers.Serializer):
    correo = serializers.EmailField()

    def validate_correo(self, value):
        try:
            usuario = Usuario.objects.get(correo=value)
            if not usuario.is_active:
                raise serializers.ValidationError("Cuenta inactiva.")
            return usuario
        except Usuario.DoesNotExist:
            raise serializers.ValidationError("No existe un usuario con ese correo.")


class PasswordResetSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_token(self, value):
        try:
            usuario = Usuario.objects.get(reset_password_token=value)
            if usuario.reset_password_token_expires_at < timezone.now():
                raise serializers.ValidationError("Token expirado.")
            return value
        except Usuario.DoesNotExist:
            raise serializers.ValidationError("Token inválido.")

    def save(self):
        token = self.validated_data['token']
        new_password = self.validated_data['new_password']
        usuario = Usuario.objects.get(reset_password_token=token)
        usuario.set_password(new_password)
        usuario.reset_password_token = None
        usuario.reset_password_token_expires_at = None
        usuario.save()
