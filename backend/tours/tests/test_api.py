from __future__ import annotations

from datetime import date
from decimal import Decimal

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from tours.models import TourImage, TourItineraryDay

from .factories import create_location, create_tour


class TourDetailApiTests(APITestCase):
    def test_tour_detail_returns_price_markdown_images_and_itinerary_days(self):
        location = create_location(name="Ky Quan San", elevation_m=3046)
        tour = create_tour(
            location=location,
            title="Khám phá Ky Quan San",
            summary="Tóm tắt tour",
            description_md="## Mô tả markdown",
            itinerary_md="Legacy itinerary",
            start_date=date(2026, 2, 18),
            end_date=date(2026, 2, 19),
            price=Decimal("3290000.00"),
        )

        TourImage.objects.create(
            tour=tour,
            image_url="https://cdn.example.com/img-2.jpg",
            sort_order=2,
        )
        TourImage.objects.create(
            tour=tour,
            image_url="https://cdn.example.com/img-1.jpg",
            sort_order=1,
        )
        TourItineraryDay.objects.create(
            tour=tour,
            day_number=1,
            title="Day 1 - Lên núi",
            content_md="Nội dung day 1",
        )
        TourItineraryDay.objects.create(
            tour=tour,
            day_number=0,
            title="Day 0 - Tập trung",
            content_md="Nội dung day 0",
        )

        response = self.client.get(reverse("tour-detail", kwargs={"pk": tour.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        payload = response.json()

        self.assertEqual(payload["price"], "3290000.00")
        self.assertEqual(payload["description_md"], "## Mô tả markdown")
        self.assertEqual(payload["summary"], "Tóm tắt tour")
        self.assertEqual(payload["itinerary_md"], "Legacy itinerary")
        self.assertEqual([item["image_url"] for item in payload["images"]], [
            "https://cdn.example.com/img-1.jpg",
            "https://cdn.example.com/img-2.jpg",
        ])
        self.assertEqual([item["day_number"] for item in payload["itinerary_days"]], [0, 1])
        self.assertEqual(payload["itinerary_days"][0]["date"], "2026-02-17")
        self.assertEqual(payload["itinerary_days"][1]["date"], "2026-02-18")


class RelatedToursApiTests(APITestCase):
    def test_related_tours_excludes_current_and_inactive(self):
        location = create_location(name="Ta Chi Nhu")
        current = create_tour(location=location, title="Tour hiện tại")
        active_1 = create_tour(title="Tour active 1")
        active_2 = create_tour(title="Tour active 2")
        active_3 = create_tour(title="Tour active 3")
        create_tour(title="Tour inactive", is_active=False)

        response = self.client.get(reverse("tour-related", kwargs={"pk": current.id}), {"limit": 3})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ids = [item["id"] for item in response.json()]

        self.assertEqual(len(ids), 3)
        self.assertNotIn(current.id, ids)
        self.assertTrue(active_1.id in ids or active_2.id in ids or active_3.id in ids)

    def test_related_tours_limit_validation(self):
        current = create_tour(title="Current")
        create_tour(title="Another 1")
        create_tour(title="Another 2")

        response = self.client.get(reverse("tour-related", kwargs={"pk": current.id}), {"limit": "abc"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("limit", response.json())

        response = self.client.get(reverse("tour-related", kwargs={"pk": current.id}), {"limit": 0})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("limit", response.json())
