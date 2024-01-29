import os
from typing import Any, Dict

from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler


def custom_exception_handler(exc: Exception, context: Dict[str, Any]) -> Response:
    """
    Extend DRF's default exception handler with a custom one.

    Add specific handling for certain exception types and environment modes.
    """
    response = drf_exception_handler(exc, context)

    if isinstance(exc, ObjectDoesNotExist):
        return Response({"error": str(exc)}, status=404)

    if os.getenv("APP_ENV") == "production":
        # Replace print with appropriate logging # noqa: E800
        # logger.error("UNHANDLED EXCEPTION", exc) # noqa: E800
        return Response({"error": "An unexpected error occurred"}, status=500)

    return response
