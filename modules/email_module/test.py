from django.test import TestCase
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient

from .models import Email


class EmailServiceViewTestCases(TestCase):  # noqa: WPS214
    """Test cases for the EmailServiceView class."""

    client: APIClient

    def setUp(self) -> None:
        """Set up the test case."""
        self.client = APIClient()

    def test_create_email(self) -> None:
        """Test creating a new email."""
        request_data = {
            "email": "test@example.com",
        }
        response: Response = self.client.post(
            "/api/v1/email_service/",
            request_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Email.objects.count(), 1)

    def test_create_duplicate_email(self) -> None:
        """Test creating a duplicate email."""
        email: str = "test@example.com"
        Email.objects.create(
            email=email,
            internal_status="new",
            score=80,
            disposable=False,
        )
        request_data = {
            "email": email,
        }
        response: Response = self.client.post(
            "/api/v1/email_service/",
            request_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Email.objects.count(), 1)

    def test_create_invalid_email(self) -> None:
        """Test creating an invalid email."""
        request_data = {
            "email": "invalid_email",
        }
        response: Response = self.client.post(
            "/api/v1/email_service/",
            request_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_email_internal_status(self) -> None:
        """Test updating the internal status of an email."""
        email = Email.objects.create(
            email="test@example.com",
            internal_status="new",
            score=80,
            disposable=False,
        )
        request_data = {
            "internal_status": "processed",
        }
        response: Response = self.client.put(
            f"/api/v1/email_service/{email.id}/",
            request_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        email.refresh_from_db()
        self.assertEqual(email.internal_status, "processed")

    def test_update_nonexistent_email(self) -> None:
        """Test updating a nonexistent email."""
        request_data = {
            "internal_status": "processed",
        }
        response: Response = self.client.put(
            "/api/v1/email_service/9999/",
            request_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_partial_update_not_allowed(self) -> None:
        """Test partial update not allowed."""
        email = Email.objects.create(
            email="test@example.com",
            internal_status="new",
            score=80,
            disposable=False,
        )
        request_data = {
            "internal_status": "processed",
        }
        response: Response = self.client.patch(
            f"/api/v1/email_service/{email.id}/",
            request_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_email(self) -> None:
        """Test deleting an email."""
        email = Email.objects.create(
            email="test@example.com",
            internal_status="new",
            score=80,
            disposable=False,
        )
        response: Response = self.client.delete(f"/api/v1/email_service/{email.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Email.objects.count(), 0)

    def test_delete_nonexistent_email(self) -> None:
        """Test deleting a nonexistent email."""
        response: Response = self.client.delete("/api/v1/email_service/9999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
