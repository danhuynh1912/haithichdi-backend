from rest_framework import serializers

from .models import Tour


class LocationSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    elevation_m = serializers.IntegerField()


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
