import unicodedata

from django.db.models import Func, Q, TextField
from django.db.models.functions import Lower
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView

from .models import Booking, Location, Tour
from .serializers import (
    BookingCreateSerializer,
    BookingDetailSerializer,
    HomeFeaturedRoutesSerializer,
    HomeMomentsGallerySerializer,
    LocationSerializer,
    TourDetailSerializer,
    TourHotSerializer,
)
from .services import get_home_featured_routes_payload, get_home_moments_gallery_payload


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


class HomeFeaturedRoutesView(APIView):
    def get(self, request):
        payload = get_home_featured_routes_payload()
        serializer = HomeFeaturedRoutesSerializer(payload)
        return Response(serializer.data)


class HomeMomentsGalleryView(APIView):
    def get(self, request):
        payload = get_home_moments_gallery_payload()
        serializer = HomeMomentsGallerySerializer(payload)
        return Response(serializer.data)


class TourListView(ListAPIView):
    serializer_class = TourHotSerializer

    def get_queryset(self):
        queryset = Tour.objects.filter(is_active=True).annotate(
            title_unaccent=Lower(Unaccent("title")),
            location_unaccent=Lower(Unaccent("location__name")),
        )

        location_ids = self.request.query_params.get("location_id")
        if location_ids:
            ids = [int(x) for x in location_ids.split(",") if x.strip().isdigit()]
            if ids:
                queryset = queryset.filter(location_id__in=ids)

        search = self.request.query_params.get("search")
        if search and search.strip():
            term = _normalize_search(search)
            queryset = queryset.filter(
                Q(title_unaccent__icontains=term) | Q(location_unaccent__icontains=term)
            )

        ordering = self.request.query_params.get("ordering")
        if ordering in {"start_date", "-start_date"}:
            queryset = queryset.order_by(ordering)
        else:
            queryset = queryset.order_by("start_date")

        return queryset.prefetch_related("images").select_related("location")


def _normalize_search(value: str) -> str:
    """Lowercase and strip accents for lenient matching."""
    normalized = unicodedata.normalize("NFD", value)
    without_accents = "".join(ch for ch in normalized if unicodedata.category(ch) != "Mn")
    return without_accents.lower().strip()


class Unaccent(Func):
    """Database UNACCENT function wrapper."""

    function = "UNACCENT"
    output_field = TextField()


class TourDetailView(RetrieveAPIView):
    serializer_class = TourDetailSerializer
    queryset = (
        Tour.objects.filter(is_active=True)
        .prefetch_related("images", "itinerary_days")
        .select_related("location")
    )


class RelatedToursListView(ListAPIView):
    serializer_class = TourHotSerializer

    def get_queryset(self):
        tour_id = self.kwargs["pk"]
        limit = _parse_related_limit(self.request.query_params.get("limit"))

        return (
            Tour.objects.filter(is_active=True)
            .exclude(id=tour_id)
            .prefetch_related("images")
            .select_related("location")
            .order_by("start_date", "end_date", "id")[:limit]
        )


class BookingCreateView(CreateAPIView):
    serializer_class = BookingCreateSerializer


class BookingDetailView(RetrieveAPIView):
    serializer_class = BookingDetailSerializer
    queryset = Booking.objects.select_related("tour__location")


class BookingByIdsListView(ListAPIView):
    serializer_class = BookingDetailSerializer

    def get_queryset(self):
        ids_param = self.request.query_params.get("ids", "")
        if not ids_param.strip():
            return Booking.objects.none()

        parsed_ids = []
        for item in ids_param.split(","):
            raw = item.strip()
            if not raw:
                continue
            if not raw.isdigit():
                raise ValidationError({"ids": "Danh sách ids không hợp lệ."})
            value = int(raw)
            if value <= 0:
                continue
            if value not in parsed_ids:
                parsed_ids.append(value)

        if not parsed_ids:
            return Booking.objects.none()

        if len(parsed_ids) > 50:
            raise ValidationError({"ids": "Tối đa 50 ids mỗi request."})

        return Booking.objects.filter(id__in=parsed_ids).select_related("tour__location")


def _parse_related_limit(raw_limit: str | None) -> int:
    if raw_limit is None:
        return 12
    raw_limit = raw_limit.strip()
    if not raw_limit:
        return 12
    if not raw_limit.isdigit():
        raise ValidationError({"limit": "Limit không hợp lệ."})

    limit = int(raw_limit)
    if limit <= 0:
        raise ValidationError({"limit": "Limit phải lớn hơn 0."})
    return min(limit, 24)
