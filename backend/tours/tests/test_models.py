from __future__ import annotations

from datetime import date
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase

from .factories import create_tour


class TourModelTests(TestCase):
    def test_end_date_must_be_greater_or_equal_start_date(self):
        tour = create_tour(start_date=date(2026, 3, 20), end_date=date(2026, 3, 18))

        with self.assertRaises(ValidationError):
            tour.full_clean()

    def test_price_and_description_markdown_persist(self):
        tour = create_tour(price=Decimal("2490000.00"), description_md="## Mô tả tour")

        refreshed = type(tour).objects.get(pk=tour.pk)
        self.assertEqual(refreshed.price, Decimal("2490000.00"))
        self.assertEqual(refreshed.description_md, "## Mô tả tour")
