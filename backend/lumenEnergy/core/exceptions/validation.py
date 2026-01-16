from .base import AppException


class DadosInvalidosException(AppException):
    default_code = "invalid_data"
    default_message = "Dados inválidos"
    status_code = 400
