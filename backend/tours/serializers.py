from rest_framework import serializers

from .models import Booking, Location, LocationAudience, Tour, TourImage, TourItineraryDay
from .services import get_itinerary_date_by_day

BOOKING_STATUS_LABELS_VI = {
    Booking.Status.PENDING: "Chờ xác nhận",
    Booking.Status.CONFIRMED: "Đã xác nhận",
    Booking.Status.CANCELLED: "Đã hủy",
}


class LocationSerializer(serializers.ModelSerializer):
    full_image_url = serializers.SerializerMethodField()
    quotation_file_url = serializers.SerializerMethodField()

    class Meta:
        model = Location
        fields = (
            "id",
            "name",
            "elevation_m",
            "description",
            "full_image_url",
            "quotation_file_url",
        )

    def get_full_image_url(self, obj: Location) -> str | None:
        return _resolve_location_image_url(obj)

    def get_quotation_file_url(self, obj: Location) -> str | None:
        if obj.quotation_file:
            return obj.quotation_file.url
        return None


class TourHotSerializer(serializers.ModelSerializer):
    location = LocationSerializer(read_only=True)
    image_url = serializers.SerializerMethodField()
    slots_left = serializers.IntegerField(read_only=True)
    booked_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Tour
        fields = (
            "id",
            "title",
            "start_date",
            "end_date",
            "location",
            "image_url",
            "slots_left",
            "booked_count",
        )

    def get_image_url(self, obj: Tour) -> str | None:
        image = obj.images.first()
        return _resolve_tour_image_url(image)


class LocationAudienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationAudience
        fields = ("id", "code", "title", "description")


class HomeFeaturedRouteSerializer(serializers.ModelSerializer):
    display_name = serializers.SerializerMethodField()
    subtitle = serializers.SerializerMethodField()
    summary = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()
    suitable_audiences = LocationAudienceSerializer(many=True, read_only=True)

    class Meta:
        model = Location
        fields = (
            "id",
            "name",
            "display_name",
            "subtitle",
            "summary",
            "image_url",
            "suitable_audiences",
        )

    def get_display_name(self, obj: Location) -> str:
        display_name = obj.home_display_name.strip()
        return display_name or obj.name

    def get_subtitle(self, obj: Location) -> str:
        return obj.home_subtitle.strip()

    def get_summary(self, obj: Location) -> str:
        summary = obj.home_feature_summary.strip()
        if summary:
            return summary
        return obj.description.strip()

    def get_image_url(self, obj: Location) -> str | None:
        return _resolve_location_image_url(obj)


class HomeAudienceLocationSerializer(serializers.ModelSerializer):
    display_name = serializers.SerializerMethodField()

    class Meta:
        model = Location
        fields = ("id", "name", "display_name")

    def get_display_name(self, obj: Location) -> str:
        display_name = obj.home_display_name.strip()
        return display_name or obj.name


class HomeHighlightAudienceSerializer(serializers.ModelSerializer):
    locations = HomeAudienceLocationSerializer(many=True, read_only=True, source="home_locations")

    class Meta:
        model = LocationAudience
        fields = ("id", "code", "title", "description", "locations")


class HomeFeaturedRoutesSerializer(serializers.Serializer):
    routes = HomeFeaturedRouteSerializer(many=True)
    highlight_audience = HomeHighlightAudienceSerializer(allow_null=True)


class HomeMomentsGalleryImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    tour_title = serializers.CharField(source="tour.title", read_only=True)
    location_name = serializers.CharField(source="tour.location.name", read_only=True)
    width = serializers.SerializerMethodField()
    height = serializers.SerializerMethodField()

    class Meta:
        model = TourImage
        fields = (
            "id",
            "image_url",
            "caption",
            "tour_title",
            "location_name",
            "width",
            "height",
        )

    def get_image_url(self, obj: TourImage) -> str | None:
        return _resolve_tour_image_url(obj)

    def get_width(self, obj: TourImage) -> int | None:
        width, _ = _resolve_tour_image_dimensions(obj)
        return width

    def get_height(self, obj: TourImage) -> int | None:
        _, height = _resolve_tour_image_dimensions(obj)
        return height


class HomeMomentsGallerySerializer(serializers.Serializer):
    images = HomeMomentsGalleryImageSerializer(many=True)


class TourImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = TourImage
        fields = ("id", "image_url", "caption", "sort_order")

    def get_image_url(self, obj: TourImage) -> str | None:
        return _resolve_tour_image_url(obj)


class TourItineraryDaySerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField()

    class Meta:
        model = TourItineraryDay
        fields = ("day_number", "date", "title", "content_md")

    def get_date(self, obj: TourItineraryDay) -> str | None:
        day_date = get_itinerary_date_by_day(obj.tour, obj.day_number)
        if day_date is None:
            return None
        return day_date.isoformat()


class TourDetailSerializer(TourHotSerializer):
    price = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)
    description_md = serializers.CharField(required=False, allow_blank=True)
    images = TourImageSerializer(many=True, read_only=True)
    itinerary_days = TourItineraryDaySerializer(many=True, read_only=True)

    class Meta(TourHotSerializer.Meta):
        fields = TourHotSerializer.Meta.fields + (
            "price",
            "description_md",
            "summary",
            "itinerary_md",
            "images",
            "itinerary_days",
        )


class BookingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = (
            "id",
            "tour",
            "full_name",
            "phone",
            "email",
            "note",
            "medal_name",
            "dob",
            "citizen_id",
            "status",
        )
        read_only_fields = ("id", "status")

    def validate_tour(self, tour: Tour) -> Tour:
        if not tour.is_active:
            raise serializers.ValidationError("Tour is not active.")
        if tour.slots_left <= 0:
            raise serializers.ValidationError("Tour is fully booked.")
        return tour

    def validate(self, attrs):
        tour = attrs.get("tour")
        phone = attrs.get("phone")
        medal_name = attrs.get("medal_name")
        dob = attrs.get("dob")
        citizen_id = attrs.get("citizen_id")

        missing = []
        if not medal_name:
          missing.append("medal_name")
        if not dob:
          missing.append("dob")
        if not citizen_id:
          missing.append("citizen_id")
        if missing:
          raise serializers.ValidationError(
              {field: "Trường này là bắt buộc." for field in missing}
          )

        if tour and phone:
            exists = Booking.objects.filter(tour=tour, phone=phone).exists()
            if exists:
                raise serializers.ValidationError(
                    {"phone": "Số điện thoại đã đăng ký tour này."}
                )
        return attrs


class BookingTourSummarySerializer(serializers.ModelSerializer):
    location = LocationSerializer(read_only=True)

    class Meta:
        model = Tour
        fields = ("id", "title", "start_date", "end_date", "location")


class BookingDetailSerializer(serializers.ModelSerializer):
    tour = BookingTourSummarySerializer(read_only=True)
    status_label = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = (
            "id",
            "tour",
            "full_name",
            "phone",
            "email",
            "note",
            "medal_name",
            "dob",
            "citizen_id",
            "status",
            "status_label",
            "created_at",
        )

    def get_status_label(self, obj: Booking) -> str:
        return BOOKING_STATUS_LABELS_VI.get(obj.status, obj.get_status_display())


def _resolve_tour_image_url(image: TourImage | None) -> str | None:
    if image is None:
        return None
    if image.image:
        return image.image.url
    return image.image_url or None


def _resolve_tour_image_dimensions(image: TourImage | None) -> tuple[int | None, int | None]:
    if image is None or not image.image:
        return None, None

    try:
        return image.image.width, image.image.height
    except (FileNotFoundError, OSError, ValueError):
        return None, None


def _resolve_location_image_url(location: Location) -> str | None:
    if location.image:
        return location.image.url
    return location.image_url or None
