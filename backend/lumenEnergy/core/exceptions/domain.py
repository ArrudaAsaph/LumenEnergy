from .base import AppException


class RecursoJaExisteException(AppException):
    default_code = "resource_already_exists"
    default_message = "Recurso já existente"
    status_code = 409


class RecursoNaoEncontradoException(AppException):
    default_code = "resource_not_found"
    default_message = "Recurso não encontrado"
    status_code = 404


class RegraNegocioException(AppException):
    default_code = "business_rule_violation"
    default_message = "Violação de regra de negócio"
    status_code = 400
