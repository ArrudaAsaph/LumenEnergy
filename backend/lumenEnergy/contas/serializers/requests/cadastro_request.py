from rest_framework import serializers
from contas.models import Usuario, Pessoa



class CadastroUsuarioRequest(serializers.Serializer):
    username = serializers.CharField(
        max_length=150,
        required=False,
        allow_blank=True
    )

    email = serializers.EmailField(
        required=True
    )

    password = serializers.CharField(
        write_only=True,
        min_length=8,
        required=True
    )

    tipo_usuario = serializers.ChoiceField(
        choices=Usuario.TipoUsuario.choices,
        required=True
    )

    nome_completo = serializers.CharField(
        max_length = 255,
        required=True
        )

    cpf = serializers.CharField(
        max_length=14,
        required=True
    )

    email_contato = serializers.EmailField(
        required=False,
        allow_blank=True
    )

    telefone = serializers.CharField(
        max_length=14,
        required=True
    )

    tipo_perfil = serializers.ChoiceField(
        choices=Pessoa.TipoPerfil.choices,
        required=True
    )

    def validate(self, data):
        if not data.get("username"):
            data["username"] = data["email"]

        if not data.get("email_contato"):
            data["email_contato"] = data["email"]
        return data
    

