from rest_framework import serializers
from contas.models import Pessoa


class PessoaCreateRequest(serializers.Serializer):
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



    

class PessoaUpdateRequest(serializers.Serializer):
    primeiro_nome = serializers.CharField(max_length=50, required=False)
    ultimo_nome = serializers.CharField(max_length=50, required=False)
    email_contato = serializers.EmailField(required=False, allow_blank=True)
    telefone = serializers.CharField(max_length=14, required=False)

    tipo_status = serializers.ChoiceField(
        choices=Pessoa.StatusPessoa.choices,
        required=False
    )

    tipo_perfil = serializers.ChoiceField(
        choices=Pessoa.TipoPerfil.choices,
        required=False
    )

    def validate(self, data):
        if not data:
            raise serializers.ValidationError(
                "Você deve enviar pelo menos um campo para atualizar."
            )
        return data
