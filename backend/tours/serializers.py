from rest_framework import serializers

from .models import Booking, Location, Tour, TourImage, TourItineraryDay
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
        if obj.image:
            return obj.image.url
        return obj.image_url or None

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
