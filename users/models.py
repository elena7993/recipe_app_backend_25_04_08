from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    first_name = models.CharField(
        max_length=50,
        editable=False,
    )
    last_name = models.CharField(
        max_length=50,
        editable=False,
    )

    name = models.CharField(
        max_length=50,
    )

    avatar = models.URLField(
        null=True,
        blank=True,
    )
