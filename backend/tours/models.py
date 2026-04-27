from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q


class Tour(models.Model):
    title = models.CharField(max_length=200)
    summary = models.TextField(blank=True)
    description_md = models.TextField(blank=True, help_text="Markdown description")
    itinerary_md = models.TextField(help_text="Markdown itinerary")
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    location = models.ForeignKey(
        "Location",
        related_name="tours",
        on_delete=models.PROTECT,
    )
    max_guests = models.PositiveIntegerField()
    leaders = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="led_tours",
        blank=True,
        help_text="Assign leaders (users with role=leader)",
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.title

    def clean(self):
        super().clean()
        if self.start_date and self.end_date and self.end_date < self.start_date:
            raise ValidationError({"end_date": "Ngày kết thúc phải lớn hơn hoặc bằng ngày bắt đầu."})

    @property
    def booked_count(self) -> int:
        return self.bookings.count()

    @property
    def slots_left(self) -> int:
        return max(self.max_guests - self.booked_count, 0)


class TourItineraryDay(models.Model):
    tour = models.ForeignKey(
        Tour,
        related_name="itinerary_days",
        on_delete=models.CASCADE,
    )
    day_number = models.PositiveIntegerField(help_text="Day index. Day 0 = one day before tour start")
    title = models.CharField(max_length=255, blank=True)
    content_md = models.TextField(blank=True, help_text="Markdown itinerary content")

    class Meta:
        ordering = ["day_number"]
        constraints = [
            models.UniqueConstraint(fields=["tour", "day_number"], name="uniq_tour_itinerary_day"),
        ]

    def __str__(self) -> str:
        return f"{self.tour.title} - Day {self.day_number}"


class LocationAudience(models.Model):
    class Code(models.TextChoices):
        BEGINNER = "beginner", "Beginner"
        INTERMEDIATE = "intermediate", "Intermediate"
        PUSH_LIMIT = "push_limit", "Push Limit"

    code = models.CharField(max_length=30, choices=Code.choices, unique=True)
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "id"]

    def __str__(self) -> str:
        return self.title


class Location(models.Model):
    name = models.CharField(max_length=200, unique=True)
    elevation_m = models.PositiveIntegerField()
    image = models.ImageField(upload_to="locations/images/", null=True, blank=True)
    image_url = models.URLField(blank=True, help_text="Fallback/External URL")
    quotation_file = models.FileField(
        upload_to="locations/quotations/",
        null=True,
        blank=True,
        help_text="Upload PDF quotation file",
    )
    description = models.TextField(blank=True)
    suitable_audiences = models.ManyToManyField(
        LocationAudience,
        related_name="locations",
        blank=True,
        help_text="Suitable audiences for this location",
    )
    home_display_name = models.CharField(
        max_length=200,
        blank=True,
        help_text="Homepage display name override",
    )
    home_subtitle = models.CharField(
        max_length=200,
        blank=True,
        help_text="Homepage subtitle shown under the title",
    )
    home_feature_summary = models.TextField(
        blank=True,
        help_text="Homepage featured routes summary",
    )
    home_feature_order = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(4)],
        help_text="Homepage featured routes order from 1 to 4",
    )

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["home_feature_order"],
                condition=Q(home_feature_order__isnull=False),
                name="uniq_location_home_feature_order",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.name} ({self.elevation_m}m)"


class TourImage(models.Model):
    tour = models.ForeignKey(Tour, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="tours/images/", null=True, blank=True)
    image_url = models.URLField(blank=True)
    caption = models.CharField(max_length=200, blank=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "id"]

    def __str__(self) -> str:
        return f"{self.tour.title} - {self.image_url or self.image.name}"


class Booking(models.Model):
    medal_name = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Tên in trên huy chương",
    )
    dob = models.DateField(
        blank=True,
        null=True,
        help_text="Ngày tháng năm sinh",
    )
    citizen_id = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Căn cước công dân",
    )
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        CONFIRMED = "confirmed", "Confirmed"
        CANCELLED = "cancelled", "Cancelled"

    tour = models.ForeignKey(Tour, related_name="bookings", on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=50)
    email = models.EmailField(blank=True)
    note = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["tour", "phone"], name="uniq_booking_phone_per_tour"),
        ]
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.full_name} - {self.tour.title}"
