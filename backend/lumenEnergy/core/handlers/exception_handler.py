from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError

from core.exceptions.base import AppException
from core.exceptions.system import SystemError
from core.exceptions import PermissaoNegadaException, RecursoJaExisteException
from core.logging.utils import log_exception


def global_exception_handler(exc, context):
    request = context.get("request")

    # 1. Exceções da aplicação derivadas de AppException
    if isinstance(exc, AppException):
        log_exception(exc, request)
        return Response(
            {
                "error": {
                    "code": getattr(exc, "code", "app_error"),
                    "message": getattr(exc, "message", str(exc)),
                    "context": getattr(exc, "context", {}),
                }
            },
            status=getattr(exc, "status_code", 400)
        )

    # 2. Exceções específicas
    if isinstance(exc, PermissaoNegadaException):
        log_exception(exc, request)
        return Response(
            {
                "error": {
                    "code": "permission_denied",
                    "message": exc.message,
                }
            },
            status=status.HTTP_403_FORBIDDEN
        )

    if isinstance(exc, RecursoJaExisteException):
        log_exception(exc, request)
        return Response(
            {
                "error": {
                    "code": "resource_already_exists",
                    "message": exc.message,
                    "context": getattr(exc, "context", {}),
                }
            },
            status=status.HTTP_409_CONFLICT
        )

    # 3. Exceções de validação do DRF
    if isinstance(exc, ValidationError):
        log_exception(exc, request)
        return Response(
            {
                "error": {
                    "code": "validation_error",
                    "message": exc.detail,
                }
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # 4. Exceções tratadas pelo DRF que não entraram nos casos acima
    response = drf_exception_handler(exc, context)
    if response is not None:
        return response

    # 5. Erro inesperado (500)
    system_exc = SystemError(
        context={
            "exception": str(exc)
        }
    )
    log_exception(system_exc, request)
    return Response(
        {
            "error": {
                "code": system_exc.code,
                "message": system_exc.message
            }
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )
