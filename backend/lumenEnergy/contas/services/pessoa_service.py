from contas.models import Pessoa
from contas.filtros import PessoaFilter
from core.services import ServiceBase

from core.exceptions import *

class PessoaService(ServiceBase):
    model = Pessoa
    domain = "contas"
    entity = "Pessoa"

    @classmethod
    def _listar_por_categoria(cls, usuario_logado):
        empresa = usuario_logado.empresa_atual


        if usuario_logado.tipo_usuario == "EMPRESA":

            perfis_visiveis = [
                Pessoa.TipoPerfil.GERENTE,
                Pessoa.TipoPerfil.ANALISTA,
                Pessoa.TipoPerfil.FINANCEIRO,
                Pessoa.TipoPerfil.INVESTIDOR,
                Pessoa.TipoPerfil.CLIENTE
            ]
        else:
            tipo = usuario_logado.pessoa.tipo_perfil

            PERFIS_VISIVEIS = {
                Pessoa.TipoPerfil.GERENTE: [
                    Pessoa.TipoPerfil.ANALISTA,
                    Pessoa.TipoPerfil.FINANCEIRO,
                    Pessoa.TipoPerfil.CLIENTE,
                ],
                Pessoa.TipoPerfil.ANALISTA: [
                    Pessoa.TipoPerfil.CLIENTE,
                ],
                Pessoa.TipoPerfil.FINANCEIRO: [
                    Pessoa.TipoPerfil.CLIENTE,
                ]
            }

            perfis_visiveis = PERFIS_VISIVEIS.get(tipo)

        if not perfis_visiveis:
            raise PermissaoNegadaException("Usuário não possui permissão para listar pessoas")
        
        pessoas = (
            Pessoa.objects
            .filter(
                empresa = empresa,
                tipo_perfil__in = perfis_visiveis
            )
        )
    
        
        print(pessoas)
        return pessoas



    @classmethod
    def listar(cls, *, usuario_logado, filtros_data=None):

        return cls._listar_por_categoria(usuario_logado = usuario_logado)

        
