from django.db import models


STRING_LENGTH_SHORT = 256
STRING_LENGTH_MEDIUM = 1024
STRING_LENGTH_LONG = 16384


class RijpModelBase(models.Model):
    created = models.DateTimeField(
        auto_now_add=True
    )
    modified = models.DateField(
        null=True,
        blank=True
    )
    deleted = models.DateField(
        null=True,
        blank=True
    )


class Project(RijpModelBase):
    name = models.CharField(
        max_length=STRING_LENGTH_SHORT
    )
