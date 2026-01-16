from rest_framework import serializers 
from contas.models import Usuario


class UsuarioCreateRequest(serializers.Serializer):
    username = serializers.CharField(
        max_length=150,
        required=True
    )

    email = serializers.EmailField(
        required=True
    )

    password = serializers.CharField(
        write_only = True,
        min_length = 8,
        required = True
    )



class UsuarioUpdateRequest(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=False)
    email = serializers.EmailField(required=False)
    desativar = serializers.BooleanField(required=False)
    ativar = serializers.BooleanField(required=False)

    def validate(self, data):
        if data.get("desativar") and data.get("ativar"):
            raise serializers.ValidationError(
                "Não é possível ativar e desativar ao mesmo tempo."
            )
        if not data:
            raise serializers.ValidationError(
                "Você deve enviar pelo menos um campo para atualizar."
            )
        return data
