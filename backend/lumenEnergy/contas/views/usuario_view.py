from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi

from contas.serializers import (
    UsuarioCreateRequest,
    UsuarioUpdateRequest,
    UsuarioResponse
)
from contas.services import UsuarioService
from contas.filtros import UsuarioFilter


class UsuarioView(APIView):

    # ========================
    # CREATE
    # ========================
    @swagger_auto_schema(
        operation_summary="Criar usuário",
        request_body=UsuarioCreateRequest,
        responses={201: UsuarioResponse},
        tags=["Usuários"],
    )
    def post(self, request):
        serializer = UsuarioCreateRequest(data=request.data)
        serializer.is_valid(raise_exception=True)

        usuario = UsuarioService.criar(data=serializer.validated_data)
        return Response(
            UsuarioResponse(usuario).data,
            status=status.HTTP_201_CREATED
        )
    
    @swagger_auto_schema(
    operation_summary="Listar usuários",
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
    responses={200: UsuarioResponse(many=True)},
    tags=["Usuários"],
)

    def get(self, request):

        usuarios = UsuarioService.listar(
            filtros_data=request.query_params
        )


        return Response(
            UsuarioResponse(usuarios, many=True).data,
            status=status.HTTP_200_OK
        )

class UsuarioDetalheView(APIView):
    # ========================
    # LIST
    # ========================
    @swagger_auto_schema(
        operation_summary="Listar usuário por id",
        responses={200: UsuarioResponse(many=True)},
        tags=["Usuários"],
    )
    def get(self, request, id=None):

        # GET /usuarios/{id}
        if id:
            usuario = UsuarioService.buscar_por_id(id=id)
            return Response(
                UsuarioResponse(usuario).data,
                status=status.HTTP_200_OK
            )

        # GET /usuarios
        usuarios = UsuarioService.listar()
        return Response(
            UsuarioResponse(usuarios, many=True).data,
            status=status.HTTP_200_OK
        )

    # ========================
    # UPDATE (dados)
    # ========================
    @swagger_auto_schema(
        operation_summary="Atualizar usuário",
        request_body=UsuarioUpdateRequest,
        responses={200: UsuarioResponse},
        tags=["Usuários"],
    )
    def put(self, request, id):
        serializer = UsuarioUpdateRequest(data=request.data)
        serializer.is_valid(raise_exception=True)

        usuario = UsuarioService.atualizar(
            id=id,
            data=serializer.validated_data
        )

        return Response(
            UsuarioResponse(usuario).data,
            status=status.HTTP_200_OK
        )

    # ========================
    # ATIVAR / DESATIVAR
    # ========================
    @swagger_auto_schema(
        operation_summary="Ativar ou desativar usuário",
        request_body=UsuarioUpdateRequest,
        responses={200: UsuarioResponse},
        tags=["Usuários"],
    )
    def patch(self, request, id):
        serializer = UsuarioUpdateRequest(data=request.data)
        serializer.is_valid(raise_exception=True)

        usuario = UsuarioService.atualizar(
            id=id,
            data=serializer.validated_data
        )

        return Response(
            UsuarioResponse(usuario).data,
            status=status.HTTP_200_OK
        )
