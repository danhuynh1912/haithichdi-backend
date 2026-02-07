from rest_framework.generics import ListAPIView

from .models import User
from .serializers import LeaderSerializer


class LeaderListView(ListAPIView):
    serializer_class = LeaderSerializer

    def get_queryset(self):
        return (
            User.objects.filter(role=User.Roles.LEADER, is_active=True)
            .order_by("first_name", "last_name", "id")
        )
