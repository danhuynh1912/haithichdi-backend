from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.db import models


class User(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = "admin", "Admin"
        LEADER = "leader", "Leader"
        CUSTOMER = "customer", "Customer"

    class RelationshipStatus(models.TextChoices):
        SINGLE = "single", "Single"
        MARRIED = "married", "Married"
        COMPLICATED = "complicated", "Complicated"
        HIDDEN = "hidden", "Hidden"

    role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.CUSTOMER)
    avatar = models.ImageField(upload_to="users/avatars/", null=True, blank=True)
    avatar_url = models.URLField(blank=True)
    bio = models.TextField(blank=True)
    strengths = ArrayField(models.CharField(max_length=100), default=list, blank=True)
    display_role = models.CharField(max_length=100, blank=True)
    relationship_status = models.CharField(
        max_length=20, choices=RelationshipStatus.choices, blank=True
    )
    date_of_birth = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=150, blank=True)
    highlight = models.TextField(blank=True)
    years_experience = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.username} ({self.role})"
