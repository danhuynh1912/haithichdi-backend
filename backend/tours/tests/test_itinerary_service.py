from __future__ import annotations

from datetime import date

from django.test import TestCase

from tours.models import TourItineraryDay
from tours.services import (
    build_default_day_title,
    get_itinerary_date_by_day,
    get_required_itinerary_day_numbers,
    sync_itinerary_days_for_tour,
)

from .factories import create_tour


class ItineraryServiceTests(TestCase):
    def test_get_required_itinerary_day_numbers_includes_day_zero(self):
        tour = create_tour(start_date=date(2026, 2, 18), end_date=date(2026, 2, 19))

        self.assertEqual(get_required_itinerary_day_numbers(tour), [0, 1, 2])

    def test_get_required_itinerary_day_numbers_empty_when_date_missing(self):
        tour = create_tour(start_date=None, end_date=None)

        self.assertEqual(get_required_itinerary_day_numbers(tour), [])

    def test_get_itinerary_date_by_day_zero_is_previous_day(self):
        tour = create_tour(start_date=date(2026, 2, 18), end_date=date(2026, 2, 19))

        self.assertEqual(get_itinerary_date_by_day(tour, 0), date(2026, 2, 17))
        self.assertEqual(get_itinerary_date_by_day(tour, 1), date(2026, 2, 18))

    def test_build_default_day_title_contains_calendar_date(self):
        tour = create_tour(start_date=date(2026, 2, 18), end_date=date(2026, 2, 18))

        self.assertEqual(build_default_day_title(tour, 0), "Day 0 - 17/02/2026")
        self.assertEqual(build_default_day_title(tour, 1), "Day 1 - 18/02/2026")

    def test_sync_itinerary_days_creates_missing_days(self):
        tour = create_tour(start_date=date(2026, 2, 18), end_date=date(2026, 2, 19))

        sync_itinerary_days_for_tour(tour)

        days = list(TourItineraryDay.objects.filter(tour=tour).order_by("day_number"))
        self.assertEqual([item.day_number for item in days], [0, 1, 2])
        self.assertEqual(days[0].title, "Day 0 - 17/02/2026")
        self.assertEqual(days[1].title, "Day 1 - 18/02/2026")
        self.assertEqual(days[2].title, "Day 2 - 19/02/2026")

    def test_sync_itinerary_days_preserves_existing_content_within_range(self):
        tour = create_tour(start_date=date(2026, 2, 18), end_date=date(2026, 2, 20))
        TourItineraryDay.objects.create(
            tour=tour,
            day_number=1,
            title="Ngày trekking chính",
            content_md="Nội dung cũ",
        )

        sync_itinerary_days_for_tour(tour)

        day1 = TourItineraryDay.objects.get(tour=tour, day_number=1)
        self.assertEqual(day1.title, "Ngày trekking chính")
        self.assertEqual(day1.content_md, "Nội dung cũ")

    def test_sync_itinerary_days_removes_out_of_range_days(self):
        tour = create_tour(start_date=date(2026, 2, 18), end_date=date(2026, 2, 20))
        sync_itinerary_days_for_tour(tour)
        self.assertEqual(TourItineraryDay.objects.filter(tour=tour).count(), 4)

        tour.end_date = date(2026, 2, 18)
        tour.save(update_fields=["end_date"])
        sync_itinerary_days_for_tour(tour)

        self.assertEqual(
            list(TourItineraryDay.objects.filter(tour=tour).values_list("day_number", flat=True)),
            [0, 1],
        )
