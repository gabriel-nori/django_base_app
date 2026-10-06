from api.utils import get_client_ip
from logger import Logger
import time

logger = Logger("request")


class RequestLogMiddleware:
    """
    Logs every API request through the Logger (and so into the database when
    LOG_TO_DB is enabled). Enabled by LOG_REQUESTS=true.
    """

    path_prefix = "/api/"

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.path.startswith(self.path_prefix):
            return self.get_response(request)

        started_at = time.monotonic()
        response = self.get_response(request)
        duration_ms = round((time.monotonic() - started_at) * 1000, 2)

        # DRF sets request.user on the underlying request after authenticating
        user = getattr(request, "user", None)
        extra = {
            "method": request.method,
            "path": request.path,
            "status": response.status_code,
            "user_id": user.pk if user and user.is_authenticated else None,
            "ip": get_client_ip(request),
            "duration_ms": duration_ms,
        }
        message = f"{request.method} {request.path} {response.status_code}"

        if response.status_code >= 500:
            logger.error(message, extra=extra)
        elif response.status_code >= 400:
            logger.warning(message, extra=extra)
        else:
            logger.info(message, extra=extra)

        return response
