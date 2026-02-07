from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Role", {"fields": ("role",)}),
        (
            "Profile",
            {
                "fields": (
                    "avatar",
                    "avatar_url",
                    "bio",
                    "strengths",
                    "display_role",
                    "relationship_status",
                    "date_of_birth",
                    "location",
                    "highlight",
                    "years_experience",
                )
            },
        ),
    )
    list_display = ("username", "email", "role", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_active")
