from typing import Any, Dict, Optional

from rest_framework import status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Email
from .serializer import CreateEmailSerializer, EmailSerializer, UpdateEmailSerializer
from .services.db_client import DatabaseClient
from .services.hunter_client.hunter_client import HunterClient
from .services.hunter_client.methods.verify_email import EmailDTO


# Create your views here.
class EmailServiceView(viewsets.ModelViewSet):
    """Viewset for managing email services."""

    queryset = Email.objects.all()
    http_method_names = ["get", "post", "put", "delete", "head", "options", "trace"]
    hunter_client = HunterClient()

    @property
    def serializer_class(self) -> Any:
        """Returns the serializer class based on the action being performed."""
        return self.serializer_classes.get(self.action, EmailSerializer)

    serializer_classes = {
        "create": CreateEmailSerializer,
        "update": UpdateEmailSerializer,
    }

    def initial(self, request: Request, *args: Any, **kwargs: Any) -> None:
        """
        Run anything that needs to occur prior to calling the method handler.

        Args:
            request (Request): The request object.
            args (Any): Positional arguments.
            kwargs (Any): Keyword arguments.
        """
        # First, run the parent's initial to set up the basics
        super().initial(request, *args, **kwargs)

        # Then perform your serialization check for every incoming request
        self.check_serialization(request)
        # Other duplicated code for every incoming request can go here

    def check_serialization(
        self,
        request: Request,
        raise_exception: bool = True,
    ) -> bool:
        """
        Check if the request data is valid.

        Args:
            request (Request): The request object.
        """
        # If the action is defined within the serializer classes, validate the request data, else return True
        if self.action in self.serializer_classes.keys():
            serializer = self.get_serializer(data=request.data)
            return serializer.is_valid(raise_exception=raise_exception)
        return True

    def create(self, request: Request) -> Response:
        """
        Create a new email record and verifies the email address.

        Args:
            request (Request): The request object.

        Returns:
            Response: The response object.
        """

        email: str = request.data.get("email")
        email_data: Optional[Dict[str, Any]] = DatabaseClient.get_email_by_address(
            email,
        )
        if email_data is not None:
            return Response(email_data, status=status.HTTP_200_OK)

        try:
            response: EmailDTO = self.hunter_client.verify_email(email)

            new_email_data: Optional[Dict[str, Any]] = DatabaseClient.store_email(
                email,
                response.status,
                response.score,
                response.disposable,
            )
            return Response(new_email_data, status=status.HTTP_201_CREATED)
        except Exception as err:
            print("err", err)  # noqa: E800
            return Response(
                {"error": "Failed to verify email"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Update the internal status of an email record.

        Args:
            request (Request): The request object.
            kwargs (Any): Additional keyword arguments.

        Returns:
            Response: The response object.
        """
        email_id: int = kwargs.get("pk")  # type: ignore
        internal_status: str = request.data.get("internal_status")
        DatabaseClient.update_email(
            email_id,
            internal_status=internal_status,
            raise_exception=True,
        )
        return Response(
            status=status.HTTP_200_OK,
        )

    # Disable unused methods
    def partial_update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Disabled partial_update method."""
        return Response(
            {"detail": "Method not allowed"},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )
