import os

from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = drf_exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if isinstance(exc, ObjectDoesNotExist):
        return Response({"error": str(exc)}, status=404)

    # If neither of the above are true and it's not 'development' mode, return a generic error and raise the exception to a log service
    if os.getenv("APP_ENV") == "production":
        # log the exception to the monitoring service (temporarily print to console)
        print("UNHANDLED EXCEPTION", exc)
        return Response({"error": "An unexpected error occurred"}, status=500)
    else:
        return response
