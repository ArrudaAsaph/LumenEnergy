from django.db import transaction
import logging
audit_logger = logging.getLogger("audit")

from contas.models import Usuario
from core.services import PermissaoService
from core.error import Erro

class UsuarioService:
    errors = []

    @classmethod
    def _erro_base(cls, usuario):
        return {
            "domain": "usuario",
            "entidade": "Usuario",
            "usuario": {
                "id": usuario.id,
                "username": usuario.username,
            },
        }
    
    @classmethod
    @transaction.atomic
    def atualizar(cls, *, usuario_logado, data):

        erro_base = cls._erro_base(usuario_logado)

        usuario = cls._buscar_por_id(
            usuario_id = data["id"],
            erro_base = erro_base
        )
        if isinstance(usuario, Erro):
            return usuario

        erro = cls._antes_atualizar(
            usuario=usuario,
            usuario_logado=usuario_logado,
            data=data,
            erro_base=erro_base
        )
        if erro:
            return erro

        # username
        if "username" in data and data["username"] != usuario.username:
            usuario.username = data["username"]

        # senha
        if data.get("antiga_password"):
            usuario.set_password(data["nova_password1"])

        # status
        if data.get("tipo_status"):
            acao = data["tipo_status"]
            if acao == Usuario.StatusUsuario.ATIVA:
                return cls._ativar(usuario, erro_base)
            if acao == Usuario.StatusUsuario.BLOQUEADA:
                return cls._bloquear(usuario, erro_base)
            

        usuario.save()

        audit_logger.info(
            "Usuário atualizado",
            extra={
                **erro_base,
                "acao": "atualizar",
                "usuario_alvo": usuario.id,
            }
        )

        return usuario

    @classmethod
    def _antes_atualizar(cls, *, usuario, usuario_logado, data, erro_base):

        erros = []

        if "username" in data:
            if Usuario.objects.filter(
                username=data["username"]
            ).exclude(id=usuario.id).exists():
                erros.append({
                    "field": "username",
                    "mensagem": "Username já em uso",
                    "value": data["username"]
                })

        if data.get("antiga_password"):
            if not data.get("nova_password1") or not data.get("nova_password2"):
                erros.append({
                    "field": "nova_password",
                    "mensagem": "Informe as duas novas senhas",
                })

            elif data["nova_password1"] != data["nova_password2"]:
                erros.append({
                    "field": "nova_password",
                    "mensagem": "As novas senhas não coincidem",
                })

            elif not usuario.check_password(data["antiga_password"]):
                erros.append({
                    "field": "antiga_password",
                    "mensagem": "Senha atual inválida",
                })


        if erros:
            return Erro(
                **erro_base,
                mensagem="Erro de validação",
                status_code=409,
                data={"erros": erros}
            )

        return None
     
    @classmethod
    def _permissao(cls, *, usuario_logado, usuario, erro_base):
        permissaoService = PermissaoService(usuario_logado)

        if usuario_logado != usuario:
            if (not permissaoService.acesso(["EMPRESA", "GERENTE"])):
                return Erro(
                **erro_base,
                mensagem = "Usuário sem permissão para atualização",
                extra = "Apenas os próprios usuários podem atualizar seus dados",
                status_code = 403
            )
        
        return True



    @classmethod
    def _buscar_por_id(cls, *, usuario_id, erro_base):


        usuario = Usuario.objects.filter(id=usuario_id).first()

        if not usuario:
            return Erro(
                **erro_base,
                acao="buscar",
                mensagem="Usuário não encontrado",
                field="id",
                value=usuario_id,
                status_code=404
            )



        return usuario

    @classmethod
    def _ativar(cls, usuario, erro_base):
        if usuario.tipo_status == Usuario.StatusUsuario.ATIVA:
            return Erro(
                **erro_base,
                acao="ativar",
                mensagem="Usuário já está ativo",
                field="tipo_status",
                value=usuario.tipo_status,
                status_code=409
            )

        usuario.tipo_status = Usuario.StatusUsuario.ATIVA
        usuario.save(update_fields=["tipo_status"])
        return usuario

    @classmethod
    def _bloquear(cls, usuario, erro_base):
        if usuario.tipo_status == Usuario.StatusUsuario.BLOQUEADA:
            return Erro(
                **erro_base,
                acao="bloquear",
                mensagem="Usuário já está bloqueado",
                field="tipo_status",
                value=usuario.tipo_status,
                status_code=409
            )

        usuario.tipo_status = Usuario.StatusUsuario.BLOQUEADA
        usuario.save(update_fields=["tipo_status"])
        return usuario