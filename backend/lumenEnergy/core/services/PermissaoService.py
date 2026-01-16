from contas.models import Pessoa, Empresa, Usuario
from core.exceptions import PermissaoNegadaException, UsuarioInativoException


class PermissaoService:
    """
    Serviço responsável por validar permissões de acesso
    respeitando a hierarquia de perfis.
    """

    HIERARQUIA = [
        "EMPRESA",
        "GERENTE",
        "ANALISTA",
        "FINANCEIRO",
        "INVESTIDOR",
        "CLIENTE",
    ]

    def __init__(self, user):
        if not user or not user.is_authenticated:
            raise PermissaoNegadaException("Usuário não autenticado")

        if user.tipo_status != Usuario.StatusUsuario.ATIVA:
            raise UsuarioInativoException("Usuário desativado")

        self.user = user

    # ------------------------------------------------------------------
    # Helpers internos
    # ------------------------------------------------------------------

    def _get_pessoa(self) -> Pessoa | None:
        try:
            return self.user.pessoa
        except Pessoa.DoesNotExist:
            return None

    def _get_empresa(self) -> Empresa | None:
        try:
            return self.user.empresa
        except Empresa.DoesNotExist:
            return None

    # ------------------------------------------------------------------
    # Perfil do usuário logado
    # ------------------------------------------------------------------

    def perfil_logado(self) -> str:
        """
        Retorna o perfil do usuário logado:
        - "EMPRESA" se for empresa ativa
        - TipoPerfil da Pessoa se for pessoa ativa
        """
        empresa = self._get_empresa()
        if empresa:
            return "EMPRESA"

        pessoa = self._get_pessoa()
        if pessoa:
            return pessoa.tipo_perfil

        raise UsuarioInativoException("Usuário sem perfil válido")

    # ------------------------------------------------------------------
    # Hierarquia
    # ------------------------------------------------------------------

    def _perfil_valido(self, perfil_logado: str, perfil_requerido: str) -> bool:
        """
        Verifica se o perfil logado possui permissão
        para o perfil requerido, respeitando hierarquia.
        """
        if perfil_logado == "EMPRESA":
            return True

        try:
            idx_logado = self.HIERARQUIA.index(perfil_logado)
            idx_requerido = self.HIERARQUIA.index(perfil_requerido)
        except ValueError:
            raise PermissaoNegadaException("Perfil inválido na hierarquia")

        return idx_logado <= idx_requerido

    # ------------------------------------------------------------------
    # API pública
    # ------------------------------------------------------------------

    def acesso(self, perfis: list[str]) -> bool:
        """
        Recebe uma lista de perfis permitidos.
        Libera se o usuário tiver qualquer um deles
        ou superior na hierarquia.
        """
        perfil = self.perfil_logado()

        for perfil_requerido in perfis:
            if self._perfil_valido(perfil, perfil_requerido):
                return True

        raise PermissaoNegadaException(
            f"Usuário '{self.user.username}' não possui permissão. "
            f"Perfis exigidos: {', '.join(perfis)}"
        )
