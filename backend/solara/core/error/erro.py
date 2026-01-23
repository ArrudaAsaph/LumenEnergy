class Erro:
    def __init__(
        self,
        domain: str,
        entidade: str,
        acao: str,
        status_code: int = 400,
        mensagem: str = "",
        field: str | None = None,
        data: dict | None = None,
        usuario: dict | None = None,
        interno: dict | None = None,
    ):
        self.domain = domain
        self.entidade = entidade
        self.acao = acao
        self.status_code = status_code
        self.mensagem = mensagem
        self.field = field
        self.data = data or {}
        self.usuario = usuario or {}
        self.interno = interno or {}

    def to_response(self):
        """O que o cliente pode ver"""
        return {
            "message": self.mensagem,
            "field": self.field,
            "data": self.data,
        }

    def to_log(self):
        """O que vai para o log"""
        return {
            "domain": self.domain,
            "entidade": self.entidade,
            "acao": self.acao,
            "status_code": self.status_code,
            "mensagem": self.mensagem,
            "field": self.field,
            "data": self.data,
            "usuario": self.usuario,
            "interno": self.interno,
        }
