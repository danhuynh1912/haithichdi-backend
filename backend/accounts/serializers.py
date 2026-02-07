from rest_framework import serializers

from .models import User


class LeaderSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    full_avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "full_name",
            "email",
            "avatar_url",
            "bio",
            "strengths",
            "display_role",
            "relationship_status",
            "date_of_birth",
            "location",
            "highlight",
            "years_experience",
            "full_avatar_url",
            "date_joined",
        )

    def get_full_name(self, obj: User) -> str:
        name = obj.get_full_name().strip()
        return name if name else obj.username

    def get_full_avatar_url(self, obj: User) -> str | None:
        if obj.avatar:
            return obj.avatar.url
        return obj.avatar_url or None
