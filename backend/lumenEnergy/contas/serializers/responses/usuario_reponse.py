from rest_framework import serializers
from contas.models import Usuario

class UsuarioResponse(serializers.ModelSerializer):

    class Meta:
        model = Usuario
        fields = [
            'id',
            'username',
            'email',
            'tipo_usuario',
            'tipo_status'
        ]

