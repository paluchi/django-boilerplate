from django.apps import AppConfig

# This is the configuration file for the email_module app.


class EmailServiceConfig(AppConfig):
    """This class represents the configuration for the email_module app."""

    default_auto_field = (
        "django.db.models.BigAutoField"  # This is the default auto field for Django.
    )
    name = "modules.email_module"  # This is the name of the app.
