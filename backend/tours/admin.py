from django.contrib import admin

from .models import Booking, Location, LocationAudience, Tour, TourImage, TourItineraryDay
from .services import sync_itinerary_days_for_tour


class TourImageInline(admin.TabularInline):
    model = TourImage
    extra = 1


class TourItineraryDayInline(admin.StackedInline):
    model = TourItineraryDay
    extra = 0
    fields = ("day_number", "title", "content_md")


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "price",
        "location",
        "start_date",
        "end_date",
        "max_guests",
        "booked_count",
        "slots_left",
        "is_active",
    )
    search_fields = ("title", "location__name")
    list_filter = ("is_active",)
    inlines = [TourImageInline, TourItineraryDayInline]
    filter_horizontal = ("leaders",)
    fields = (
        "title",
        "location",
        "summary",
        "description_md",
        "itinerary_md",
        "price",
        "start_date",
        "end_date",
        "max_guests",
        "leaders",
        "is_active",
    )

    class Media:
        js = ("tours/admin/tour_itinerary_days.js",)

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        sync_itinerary_days_for_tour(form.instance, remove_out_of_range=True)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "phone",
        "tour",
        "status",
        "created_at",
        "medal_name",
        "citizen_id",
    )
    search_fields = ("full_name", "phone", "citizen_id", "tour__title", "medal_name")
    list_filter = ("status",)


@admin.register(TourImage)
class TourImageAdmin(admin.ModelAdmin):
    list_display = ("tour", "image_url", "sort_order")
    search_fields = ("tour__title", "image_url")


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "home_feature_order", "elevation_m", "image", "image_url")
    search_fields = ("name",)
    filter_horizontal = ("suitable_audiences",)
    fields = (
        "name",
        "elevation_m",
        "description",
        "image",
        "image_url",
        "quotation_file",
        "suitable_audiences",
        "home_display_name",
        "home_subtitle",
        "home_feature_summary",
        "home_feature_order",
    )


@admin.register(LocationAudience)
class LocationAudienceAdmin(admin.ModelAdmin):
    list_display = ("title", "code", "sort_order")
    ordering = ("sort_order", "id")
    search_fields = ("title", "code")
