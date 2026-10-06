from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid


class User(AbstractUser):
    email = models.EmailField(
        max_length=254,
        unique=True,
        help_text="Email address used for authentication.",
        error_messages={
            "unique": "A user with that email already exists.",
        },
    )
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    # Use email as the username field for authentication
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]  # Required when creating a superuser

    def __str__(self):
        return self.get_full_name() or self.username
