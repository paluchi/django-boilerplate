from typing import Any, Dict, Optional

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Email
from .serializer import CreateEmailSerializer, EmailSerializer, UpdateEmailSerializer
from .services.db_client import DatabaseClient
from .services.hunter_client import HunterClient


# Create your views here.
class EmailServiceView(viewsets.ModelViewSet):
    """Viewset for managing email services."""

    queryset = Email.objects.all()
    http_method_names = ["get", "post", "put", "delete", "head", "options", "trace"]

    @property
    def serializer_class(self) -> Any:
        """Returns the serializer class based on the action being performed."""
        return self.serializer_classes.get(self.action, EmailSerializer)

    serializer_classes = {
        "create": CreateEmailSerializer,
        "update": UpdateEmailSerializer,
    }

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Create a new email record and verifies the email address.

        Args:
            request (Request): The request object.

        Returns:
            Response: The response object.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email: str = request.data.get("email")
        email_data: Optional[Dict[str, Any]] = DatabaseClient.get_email_by_address(
            email,
        )
        if email_data is not None:
            return Response(email_data, status=status.HTTP_200_OK)

        client = HunterClient()
        response: Optional[Dict[str, Any]] = client.verify_email(email)
        if response is None:
            return Response(
                {"error": "Failed to verify email"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        new_email_data: Optional[Dict[str, Any]] = DatabaseClient.store_email(
            email,
            response["status"],
            response["score"],
            response["disposable"],
        )
        return Response(new_email_data, status=status.HTTP_201_CREATED)

    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Update the internal status of an email record.

        Args:
            request (Request): The request object.
            kwargs (Any): Additional keyword arguments.

        Returns:
            Response: The response object.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email_id: int = kwargs.get("pk")  # type: ignore
        internal_status: str = request.data.get("internal_status")
        try:
            DatabaseClient.update_email(
                email_id,
                internal_status=internal_status,
                raise_exception=True,
            )
            return Response(
                status=status.HTTP_200_OK,
            )
        except ObjectDoesNotExist as error:
            return Response({"error": str(error)}, status=status.HTTP_404_NOT_FOUND)

    # Disable unused methods
    def partial_update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Disabled partial_update method."""
        return Response(
            {"detail": "Method not allowed"},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )
