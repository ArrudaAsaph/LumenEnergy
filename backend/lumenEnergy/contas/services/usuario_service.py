from django.db import transaction

from contas.models import Usuario
from contas.filtros import UsuarioFilter

from core.services import ServiceBase
from core.exceptions import (
    RecursoJaExisteException,
    RecursoNaoEncontradoException,
    DadosInvalidosException
)


class UsuarioService(ServiceBase):
    model = Usuario
    domain = "contas"
    entity = "Usuario"
    filterset_class = UsuarioFilter

    @staticmethod
    def _validar_criacao(*, data):
        base_context = {
            "domain": "contas",
            "entity": "Usuario",
            "action": "criar",
        }

        if Usuario.objects.filter(email=data["email"]).exists():
            raise RecursoJaExisteException(
                context={
                    **base_context,
                    "field": "email",
                    "value": data["email"],
                }
            )

        if Usuario.objects.filter(username=data["username"]).exists():
            raise RecursoJaExisteException(
                context={
                    **base_context,
                    "field": "username",
                    "value": data["username"],
                }
            )

        if data["tipo_usuario"] not in Usuario.TipoUsuario.values:
            raise DadosInvalidosException(
                message="Tipo de usuário inválido",
                context={
                    **base_context,
                    "field": "tipo_usuario",
                    "value": data["tipo_usuario"],
                }
            )

    @staticmethod
    def _validar_atualizacao(*, usuario, data):
        base_context = {
            "domain": "contas",
            "entity": "Usuario",
            "action": "atualizar",
        }

        if "email" in data and data["email"] != usuario.email:
            if Usuario.objects.filter(email=data["email"]).exclude(id = usuario.id).exists():
                raise RecursoJaExisteException(
                    context={
                        **base_context,
                        "field": "email",
                        "value": data["email"],
                    }
                )

        if "username" in data and data["username"] != usuario.username:
            if Usuario.objects.filter(username=data["username"]).exclude(id = usuario.id).exists():
                raise RecursoJaExisteException(
                    context={
                        **base_context,
                        "field": "username",
                        "value": data["username"],
                    }
                )
      
    @classmethod
    @transaction.atomic
    def criar(cls, *, data):
        cls._validar_criacao(data=data)

        usuario = Usuario(
            username=data["username"],
            email=data["email"],
            tipo_usuario=data["tipo_usuario"],
        )
        usuario.set_password(data["password"])
        usuario.save()

        return usuario

    @classmethod
    @transaction.atomic
    def atualizar(cls, *, id, data):
        usuario = cls.buscar_por_id(id=id)

        if data.get("desativar"):
            cls.desativar(usuario=usuario)
        elif data.get("ativar"):
            cls.ativar(usuario=usuario)

        cls._validar_atualizacao(usuario=usuario, data=data)

        if "email" in data:
            usuario.email = data["email"]
        if "username" in data:
            usuario.username = data["username"]

        usuario.save()
        return usuario

    @staticmethod
    def listar(*, filtros_data=None):
        queryset = Usuario.objects.all()

        if filtros_data:
            filtro = UsuarioFilter(
                data=filtros_data,
                queryset=queryset
            )
            return filtro.qs

        return queryset
    
    @classmethod
    def buscar_por_id(cls, *, id):
        try:
            return Usuario.objects.get(id=id)
        except Usuario.DoesNotExist:
            raise RecursoNaoEncontradoException(
                message="Usuário não encontrado",
                context={
                    "domain": "contas",
                    "entity": "Usuario",
                    "action": "buscar",
                    "field": "id",
                    "value": id,
                }
            )



    @classmethod
    @transaction.atomic
    def desativar(cls, *, usuario):
        """
        Desativa um usuário. Lança exceção se já estiver desativado.
        """
        if not usuario.ativo:
            raise RecursoJaExisteException(
                message="Usuário já está desativado",
                context={
                    "domain": "contas",
                    "entity": "Usuario",
                    "action": "desativar",
                    "field": "id",
                    "value": usuario.id,
                }
            )
        usuario.ativo = False
        usuario.save(update_fields=['ativo'])
        return usuario

    @classmethod
    @transaction.atomic
    def ativar(cls, *, usuario):
        """
        Ativa um usuário. Lança exceção se já estiver ativo.
        """
        if usuario.ativo:
            raise RecursoJaExisteException(
                message="Usuário já está ativo",
                context={
                    "domain": "contas",
                    "entity": "Usuario",
                    "action": "ativar",
                    "field": "id",
                    "value": usuario.id,
                }
            )
        usuario.ativo = True
        usuario.save(update_fields=['ativo'])
        return usuario

