from django.contrib import admin

from .models import Booking, Location, Tour, TourImage


class TourImageInline(admin.TabularInline):
    model = TourImage
    extra = 1


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = (
        "title",
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
    inlines = [TourImageInline]
    filter_horizontal = ("leaders",)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("full_name", "phone", "tour", "status", "created_at")
    search_fields = ("full_name", "phone", "tour__title")
    list_filter = ("status",)


@admin.register(TourImage)
class TourImageAdmin(admin.ModelAdmin):
    list_display = ("tour", "image_url", "sort_order")
    search_fields = ("tour__title", "image_url")


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "elevation_m")
    search_fields = ("name",)
