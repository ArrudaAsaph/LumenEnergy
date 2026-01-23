import logging

logger = logging.getLogger("core")

class Erro:
    def __init__(
        self,
        *,
        domain,
        entidade,
        acao,
        mensagem,
        extra = None,
        status_code,
        field=None,
        data=None,
        usuario=None,
        nivel_log="WARNING",
        tipo="VALIDACAO"
    ):
        self.domain = domain
        self.entidade = entidade
        self.acao = acao
        self.extra = extra
        self.mensagem = mensagem
        self.status_code = status_code
        self.field = field
        self.data = data or {}
        self.usuario = usuario
        self.tipo = tipo

        self._log(nivel_log)

    def _log(self, nivel):
        log_data = {
            "domain": self.domain,
            "entidade": self.entidade,
            "acao": self.acao,
            "field": self.field,
            "data": self.data,
            "usuario": self.usuario,
        }

        if nivel == "WARNING":
            logger.warning(self.mensagem, extra=log_data)
        elif nivel == "ERROR":
            logger.error(self.mensagem, extra=log_data)

    def to_response(self):
        return {
            "message": self.mensagem,
            "extra": self.extra,
            "field": self.field,
            "data": self.data,
        }
