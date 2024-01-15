from rest_framework import serializers

from .models import Email

# Serializers define the API representation.
# They are used to convert model instances to JSON.


class EmailSerializer(serializers.ModelSerializer):
    """Serializer for the Email model."""

    class Meta:
        model = Email
        fields = "__all__"


class CreateEmailSerializer(serializers.ModelSerializer):
    """Serializer for creating and validating email addresses."""

    email = serializers.EmailField(
        required=True,
        help_text="Email address to verify and store in database",
    )

    class Meta:
        model = Email
        fields = ["email"]


class UpdateEmailSerializer(serializers.ModelSerializer):
    """Serializer for updating the internal status of an email."""

    internal_status_choices = [
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("canceled", "Canceled"),
        ("error", "Error"),
    ]

    internal_status = serializers.ChoiceField(
        choices=internal_status_choices,
        required=True,
        help_text="Internal status of email",
    )

    class Meta:
        model = Email
        fields = ["internal_status"]
