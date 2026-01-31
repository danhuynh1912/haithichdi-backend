from rest_framework import serializers

from .models import Location, Tour


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
        if image is None:
            return None
        if image.image:
            return image.image.url
        return image.image_url or None
