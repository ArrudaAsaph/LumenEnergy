import logging

logger = logging.getLogger("lumenEnergy")


def log_exception(exc, request=None):
    log_data = {
        "error_code": exc.code,
        "message": exc.message,
        "extra": exc.extra,
        "context": exc.context,
    }

    if request:
        log_data.update({
            "path": request.path,
            "method": request.method,
            "user": getattr(request.user, "id", None),
        })

    level = exc.log_level

    getattr(logger, level)(log_data)
