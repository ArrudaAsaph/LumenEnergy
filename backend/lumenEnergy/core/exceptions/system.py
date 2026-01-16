# core/exceptions/system.py

from .base import AppException


class SystemError(AppException):
    status_code = 500
    default_code = "system_error"
    default_message = "Erro interno do sistema"
    log_level = "error"
