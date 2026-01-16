import re
from django.db import transaction
from contas.models import Usuario, Pessoa

from core.exceptions import (
    RecursoJaExisteException,
    DadosInvalidosException,
    PermissaoNegadaException)

from core.services import PermissaoService

class CadastroService:

    @staticmethod
    def _normalizar_cpf(cpf):
        return re.sub(r"\D", "", cpf or "")

    @staticmethod
    def _normalizar_telefone(telefone):
        return re.sub(r"\D", "", telefone or "")

    @staticmethod
    def _normalizar_nome(nome):
        nome = nome.split()
        primeiro_nome = nome[0].capitalize()
        ultimo_nome = nome[-1].capitalize()
        return primeiro_nome, ultimo_nome
    
    @classmethod
    def _validar_criacao_usuario(cls, *, data):
        base_context = {
            "domain": "contas",
            "entity": "Usuario",
            "action": "criar",
        }

        if Usuario.objects.filter(email=data["email"]).exists():
            raise RecursoJaExisteException(
                context={**base_context, "field": "email", "value": data["email"]}
            )

        if Usuario.objects.filter(username=data["username"]).exists():
            raise RecursoJaExisteException(
                context={**base_context, "field": "username", "value": data["username"]}
            )

        if len(data["password"]) < 8:
            raise DadosInvalidosException(
                message = "Senha deve ter no mínimo 8 caracteres",
                context = {**base_context, "field": "password"},
            )

    @classmethod
    def _validar_criacao_pessoa(cls, *, data):
        base_context = {
            "domain": "contas",
            "entity": "Pessoa",
            "action": "criar",
        }

        data["cpf"] = cls._normalizar_cpf(data["cpf"])
        data["telefone"] = cls._normalizar_telefone(data["telefone"])
        data["primeiro_nome"], data["ultimo_nome"] = cls._normalizar_nome(data["nome_completo"])
        
        if len(data["cpf"]) != 11:
            raise DadosInvalidosException(
                message="CPF inválido",
                context={**base_context, "field": "cpf", "value": data["cpf"]},
            )

        if Pessoa.objects.filter(cpf=data["cpf"]).exists():
            raise RecursoJaExisteException(
                context={**base_context, "field": "cpf", "value": data["cpf"]}
            )

        
        if Pessoa.objects.filter(email_contato=data["email_contato"]).exists():
            raise RecursoJaExisteException(
                context={
                    **base_context,
                    "field": "email_contato",
                    "value": data["email_contato"],
                }
            )

        if Pessoa.objects.filter(telefone=data["telefone"]).exists():
            raise RecursoJaExisteException(
                context={**base_context, "field": "telefone", "value": data["telefone"]}
            )

        if data["tipo_perfil"] not in Pessoa.TipoPerfil.values:
            raise DadosInvalidosException(
                message="Tipo de perfil inválido",
                context={**base_context, "field": "tipo_perfil", "value": data["tipo_perfil"]},
            )

    @classmethod
    def _validar_permissao_cadastro(cls, *, usuario_logado, tipo_perfil_novo: str):
        """
        Regras:
        - Apenas EMPRESA e GERENTE podem cadastrar usuários
        - Apenas EMPRESA pode cadastrar GERENTE
        """

        permissao = PermissaoService(usuario_logado)

        perfil_logado = permissao.perfil_logado()

        if perfil_logado not in ["EMPRESA", Pessoa.TipoPerfil.GERENTE]:
            raise PermissaoNegadaException(
                "Você não tem permissão para cadastrar usuários"
            )

        if (
            tipo_perfil_novo == Pessoa.TipoPerfil.GERENTE
            and perfil_logado != "EMPRESA"
        ):
            raise PermissaoNegadaException(
                "Apenas empresas podem cadastrar gerentes"
            )

    @classmethod
    @transaction.atomic
    def criar(cls, *, data, usuario_logado):
        cls._validar_permissao_cadastro(
            usuario_logado=usuario_logado,
            tipo_perfil_novo=data["tipo_perfil"]
        )
        print("cheguei")
        empresa = usuario_logado.empresa_responsavel
        print("sai")
            
        cls._validar_criacao_usuario(data = data)
        cls._validar_criacao_pessoa(data = data)

        usuario = Usuario(
            username=data["username"],
            email=data["email"],
            tipo_usuario="PESSOA",
        )
        usuario.set_password(data["password"])
        usuario.save()

        pessoa = Pessoa(
            primeiro_nome=data.get("primeiro_nome", ""),
            ultimo_nome=data.get("ultimo_nome", ""),
            nome_completo=data["nome_completo"],
            cpf=data["cpf"],                     
            email_contato=data.get("email_contato", ""),
            telefone=data["telefone"],          
            tipo_perfil=data["tipo_perfil"],
            empresa=empresa,
            usuario=usuario,
            criado_por = usuario_logado,
        )

        pessoa.save()

        return usuario