#COdigo 24
# Este archivo tiene por objetivo definir la estructura y las reglas de validación para los datos relacionados con los usuarios en las operaciones de la API.
from rest_framework import serializers
from .models import Usuario


class UsuarioParcialSerializer(serializers.ModelSerializer):
    """Serializador para actualizar parcialmente un usuario (PATCH)."""

    class Meta:
        model = Usuario
        fields = [
            'username',
            'password',
            'date_of_birth',
            'first_name',
            'last_name',
            'email'
        ]
        extra_kwargs = {
            field: {'required': False}
            for field in fields
        }

    @staticmethod
    def validar_username(username):
        """Valida que el username no tenga más de 20 caracteres."""
        if len(username) > 20:
            raise serializers.ValidationError(
                "El nombre de usuario no puede tener más de 20 caracteres."
            )
        return username