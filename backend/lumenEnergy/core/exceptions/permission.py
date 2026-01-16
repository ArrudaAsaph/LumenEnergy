from .base import AppException


class PermissaoNegadaException(AppException):
    default_code = "permission_denied"
    default_message = "Permissão negada"
    status_code = 403


class UsuarioInativoException(AppException):
    default_code = "inactive_user"
    default_message = "Usuário inativo"
    status_code = 403
