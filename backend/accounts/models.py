from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = "admin", "Admin"
        LEADER = "leader", "Leader"
        CUSTOMER = "customer", "Customer"

    role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.CUSTOMER)

    def __str__(self) -> str:
        return f"{self.username} ({self.role})"
