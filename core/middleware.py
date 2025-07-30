import logging
from datetime import datetime

logger = logging.getLogger("request_logger")


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        user = request.user if request.user.is_authenticated else "Anonymous"
        phone = getattr(user, "phone_number", user)  # Agar user modelda phone bo‘lsa

        now = datetime.now().strftime("[%d/%b/%Y %H:%M:%S]")
        method = request.method
        path = request.get_full_path()
        status = response.status_code

        log_msg = f"{now} {method} {path} Status: {status} User: {phone}"
        logger.info(log_msg)

        return response
