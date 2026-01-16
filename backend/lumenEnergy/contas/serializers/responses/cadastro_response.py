from rest_framework import serializers
from .usuario_reponse import UsuarioResponse
from .pessoa_response import PessoaResponse


class CadastroResponse(serializers.Serializer):
    usuario = UsuarioResponse()
    pessoa = PessoaResponse()
