from django.db.models import Q
from rest_framework_simplejwt.tokens import RefreshToken

from core.error import Erro
from contas.models import Usuario


class LoginService:

    @staticmethod
    def login(*, data):

        username = data["username"]
        password = data["password"]

        usuario = Usuario.objects.filter(
            Q(username=username) | Q(email=username)
        ).first()

        erro_base = {
            "domain": "autenticacao",
            "entidade": "Usuario",
            "acao": "login",
        }

        if not usuario or not usuario.check_password(password):
            return Erro(
                **erro_base,
                mensagem="Usuário ou senha inválidos",
                status_code=401,
                field="credentials",
                data={
                    "username": username
                }
            )

        if usuario.tipo_status != Usuario.StatusUsuario.ATIVA:
            return Erro(
                **erro_base,
                mensagem="Usuário está bloqueado",
                status_code=403,
                field="status",
                data={
                    "status": usuario.tipo_status
                }
            )

        refresh = RefreshToken.for_user(usuario)

        retorno = {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }

        if usuario.tipo_usuario == "PERFIL":
            retorno["pessoa"] = usuario.pessoa
        else:
            retorno["empresa"] = usuario.empresa

        return retorno
