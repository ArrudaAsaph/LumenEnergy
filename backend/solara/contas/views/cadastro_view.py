from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.permissions import IsAuthenticated

from contas.serializers import (
    CadastroUsuarioRequest,
    PessoaResponse
)
from contas.services import CadastroService


class CadastroView(APIView):
    

    @swagger_auto_schema(
        operation_summary="Cadastra uma pessoa",
        request_body = CadastroUsuarioRequest,
        responses = {201: PessoaResponse},
        tags=["Cadastro"],
    )
    
    def post(self, request):
        serializer = CadastroUsuarioRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        usuario = CadastroService.criar(data=serializer.validated_data, usuario_logado = request.user)
        
        response_serializer = PessoaResponse({
            "usuario": usuario,
            "pessoa": usuario.pessoa
            })
        
        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
        )
    
    