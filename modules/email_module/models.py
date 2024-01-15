from django.db import models

# Models are orm objects that represent a table in the database.
# The ORM is a layer that allows us to interact with the database without writing queries.


class Email(models.Model):
    """Represents an email address."""

    objects = models.Manager()  # noqa WPS110
    id = models.AutoField(primary_key=True)

    email = models.EmailField(unique=True, blank=False, null=False)
    status = models.CharField(max_length=200, blank=False, null=False)
    score = models.FloatField(null=False, blank=False)
    disposable = models.BooleanField(default=False, blank=True)
    domain = models.CharField(max_length=200, blank=True)
    domain_score = models.FloatField(null=True, blank=True)
    company = models.CharField(max_length=200, blank=True, null=True)
    position = models.CharField(max_length=200, blank=True, null=True)
    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    internal_status = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        default="pending",
    )

    def __str__(self) -> str:
        """Return a string representation of the Email object."""
        return self.email
