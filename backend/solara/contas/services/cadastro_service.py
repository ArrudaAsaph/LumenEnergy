import re
from django.db import transaction

from core.error import Erro

from contas.models import Usuario, Pessoa



class CadastroService():
    
    @classmethod
    @transaction.atomic
    def criar(cls, *, usuario_logado, data):
        erro = cls._antes_criar(
            usuario_logado = usuario_logado,
            data = data
        )

        if erro:
            return erro
        
        novo_usuario = Usuario(
            username = data["username"],
            email = data["email"],
        )

        novo_usuario.set_password(data["password"])

        novo_usuario.save()

        
        nova_pessoa = Pessoa(
            primeiro_nome = data["primeiro_nome"],
            ultimo_nome = data["ultimo_nome"],
            nome_completo = data["nome_completo"],
            cpf = data["cpf"],                     
            email_contato = data["email_contato"],
            telefone = data["telefone"],          
            tipo_perfil=data["tipo_perfil"],
            empresa = usuario_logado.empresa_vinculada,
            usuario = novo_usuario,
            criado_por = usuario_logado,
        )

        nova_pessoa.save()

        return nova_pessoa
        
    
    
    @classmethod
    def _antes_criar(cls, *, usuario_logado, data):
        erro_base = {
            "domain": "cadastro",
            "entidade": "Pessoa",
            "acao": "criar",
            "usuario": {
                "id": usuario_logado.id,
                "username": usuario_logado.username,
            },
        }

        data["cpf"] = cls._normalizar_cpf(data["cpf"])
        data["telefone"] = cls._normalizar_telefone(data["telefone"])
        data["primeiro_nome"], data["ultimo_nome"] = cls._normalizar_nome(data["nome_completo"])

        cls._validar(data = data, erro_base = erro_base)   
    @classmethod
    def _validar(cls, *, data, erro_base):
        
        # Usuario
        if Usuario.objects.filter(username = data["username"]).exists():
            return Erro(
                **erro_base,
                mensagem = "Usuário já existente",
                field = "username",
                status_code = 409,
                data = {
                    "username" : data["username"]
                }
            )
        
        if Usuario.objects.filter(email = data["email"]).exists():
            return Erro(
                **erro_base,
                mensagem = "Usuário já existente",
                field = "email",
                status_code = 409,
                data = {
                    "email" : data["email"]
                }
            )
        
        if Usuario.objects.filter(username = data["username"]).exists():
            return Erro(
                **erro_base,
                mensagem = "Usuário já existente",
                field = "username",
                status_code = 409,
                data = {
                    "username" : data["username"]
                }
            )

        # Pessoa
        if Pessoa.objects.filter(cpf = data["cpf"]).exists():
            return Erro(
                **erro_base,
                mensagem = "Usuário já existente",
                field = "cpf",
                status_code = 409,
                data = {
                    "cpf" : data["cpf"]
                }
            )
        
        if Pessoa.objects.filter(email_contato = data["email_contato"]).exists():
            return Erro(
                **erro_base,
                mensagem = "Usuário já existente",
                field = "email_contato",
                status_code = 409,
                data = {
                    "email_contato" : data["email_contato"]
                }
            )
        
        if Pessoa.objects.filter(telefone = data["telefone"]).exists():
            return Erro(
                **erro_base,
                mensagem = "Usuário já existente",
                field = "telefone",
                status_code = 409,
                data = {
                    "telefone" : data["telefone"]
                }
            )
    
        return None
    # Normalização

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
