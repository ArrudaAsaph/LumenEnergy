from rest_framework import serializers
from contas.models import Pessoa

class PessoaResponse(serializers.ModelSerializer):

    class Meta:
        model = Pessoa
        fields = [
            'id',
            'primeiro_nome',
            'ultimo_nome',
            'tipo_perfil'
        ]

