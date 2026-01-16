from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from contas.serializers import PessoaResponse
from contas.services import PessoaService


class PessoaView(APIView):

    @swagger_auto_schema(
        operation_summary="Listar pessoas",
        manual_parameters=[
            openapi.Parameter(
                "username",
                openapi.IN_QUERY,
                description="Filtrar por username (contém)",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "email",
                openapi.IN_QUERY,
                description="Filtrar por email (contém)",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "tipo_usuario",
                openapi.IN_QUERY,
                description="Tipo do usuário",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "ativo",
                openapi.IN_QUERY,
                description="Usuário ativo",
                type=openapi.TYPE_BOOLEAN,
            ),
        ],
        responses={200: PessoaResponse(many=True)},
        tags=["Pessoa"],
    )
    def get(self, request):
        pessoas = PessoaService.listar(
            usuario_logado = request.user,
            filtros_data=request.query_params
        )



        return Response(
            PessoaResponse(pessoas, many=True).data,
            status=status.HTTP_200_OK
        )
