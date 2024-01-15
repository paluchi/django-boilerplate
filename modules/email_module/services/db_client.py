from typing import Any, Dict, Optional

from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError, models
from django.forms.models import model_to_dict

from ..models import Email


class DatabaseClient:
    """A class that provides database operations for email objects."""

    @staticmethod
    def get_email_by_address(
        email: str,
        raise_exception: bool = False,
    ) -> Optional[Dict[str, Any]]:
        """Get email by address."""
        try:
            email_instance = Email.objects.get(email=email)
            return model_to_dict(email_instance)
        except Email.DoesNotExist:
            if raise_exception:
                raise Email.DoesNotExist(f"Email with address {email} does not exist.")
            return None

    @staticmethod
    def get_email_by_id(
        email_id: int,
        raise_exception: bool = False,
    ) -> Optional[Dict[str, Any]]:
        """Get email by ID."""
        try:
            email_instance = Email.objects.get(pk=email_id)
            return model_to_dict(email_instance)
        except ObjectDoesNotExist:
            if raise_exception:
                raise ObjectDoesNotExist(f"Email with id {email_id} does not exist.")
            return None

    @staticmethod
    def update_email(
        email_id: int,
        raise_exception: bool = False,
        **update_params: Any,
    ) -> Optional[Email]:
        """Update email."""
        try:
            email_obj: Email = Email.objects.get(pk=email_id)
            for key, update_val in update_params.items():
                setattr(email_obj, key, update_val)
            email_obj.save()
            return email_obj
        except Email.DoesNotExist:
            if raise_exception:
                raise ObjectDoesNotExist(f"Email with id {email_id} does not exist.")
            return None

    @staticmethod
    def store_email(
        email: str,
        status: str,
        score: float,
        disposable: bool,
        raise_exception: bool = False,
    ) -> Optional[Dict[str, Any]]:
        """Store email."""
        try:
            store_params = {
                "email": email,
                "status": status,
                "score": score,
                "disposable": disposable,
            }
            email_obj, created = Email.objects.get_or_create(
                email=email,
                defaults=store_params,
            )
            return model_to_dict(email_obj)
        except IntegrityError:
            if raise_exception:
                raise IntegrityError(f"Email {email} is already in use.")
            return None

    # Example methods for retrieving collections of emails
    @staticmethod
    def get_all_emails() -> models.QuerySet:
        """Get all emails."""
        return Email.objects.all()

    @staticmethod
    def get_all_emails_by_status(status: str) -> models.QuerySet:
        """Get all emails by status."""
        return Email.objects.filter(status=status)
