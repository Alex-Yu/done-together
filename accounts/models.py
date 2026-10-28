from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Parent identity reserved before initial migrations; workflows follow later."""

    email = models.EmailField(unique=True)
