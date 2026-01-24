from django.utils import timezone
from rest_framework.generics import ListAPIView

from .models import Location, Tour
from .serializers import LocationSerializer, TourHotSerializer


class HotTourListView(ListAPIView):
    serializer_class = TourHotSerializer

    def get_queryset(self):
        today = timezone.localdate()
        return (
            Tour.objects.filter(
                is_active=True,
                start_date__isnull=False,
                start_date__gte=today,
                end_date__isnull=False,
            )
            .select_related("location")
            .prefetch_related("images")
            .order_by("start_date", "end_date", "id")[:10]
        )


class LocationListView(ListAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class TourListView(ListAPIView):
    serializer_class = TourHotSerializer

    def get_queryset(self):
        queryset = Tour.objects.filter(is_active=True).order_by("start_date")
        location_id = self.request.query_params.get("location_id")
        if location_id:
            queryset = queryset.filter(location_id=location_id)
        return queryset.prefetch_related("images").select_related("location")
