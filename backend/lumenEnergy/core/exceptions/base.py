import logging

logger = logging.getLogger("domain")


class AppException(Exception):
    status_code = 400
    default_code = "application_error"
    default_message = "Erro na aplicação"
    log_level = "warning"

    def __init__(
        self,
        message=None,
        code=None,
        extra=None,
        context=None
    ):
        self.message = message or self.default_message
        self.code = code or self.default_code
        self.extra = extra or {}
        self.context = context or {}

        log = getattr(logger, self.log_level, logger.warning)
        log(self.code, extra={**self.extra, **self.context})

        super().__init__(self.message)
