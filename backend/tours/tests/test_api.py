from __future__ import annotations

from datetime import date
from decimal import Decimal

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from tours.models import TourImage, TourItineraryDay

from .factories import create_location, create_location_audience, create_tour


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


class HomeFeaturedRoutesApiTests(APITestCase):
    def test_home_featured_routes_returns_ordered_locations_with_highlight_audience(self):
        beginner = create_location_audience(
            code="beginner",
            title="Người mới",
            description="Làm quen với trekking.",
            sort_order=1,
        )
        intermediate = create_location_audience(
            code="intermediate",
            title="Trung cấp",
            description="Đã có nền tảng vận động.",
            sort_order=2,
        )
        push_limit = create_location_audience(
            code="push_limit",
            title="Người muốn vượt giới hạn",
            description="Hành trình chinh phục đỉnh cao, thử thách thể lực và ý chí rõ ràng nhất.",
            sort_order=3,
        )

        alpha = create_location(
            name="Alpha",
            description="Alpha description",
            home_display_name="Alpha Ridge",
            home_subtitle="Alpha subtitle",
            home_feature_order=1,
        )
        alpha.suitable_audiences.set([beginner, intermediate])
        create_tour(location=alpha, title="Tour Alpha")

        beta = create_location(
            name="Beta",
            description="Beta description",
            home_display_name="Beta Peak",
            home_subtitle="Beta subtitle",
            home_feature_summary="Beta summary",
            home_feature_order=2,
        )
        beta.suitable_audiences.set([intermediate])
        create_tour(location=beta, title="Tour Beta")

        delta = create_location(
            name="Delta",
            description="Delta description",
            home_subtitle="Delta subtitle",
        )
        delta.suitable_audiences.set([push_limit])
        create_tour(location=delta, title="Tour Delta")

        epsilon = create_location(
            name="Epsilon",
            description="Epsilon description",
            home_subtitle="Epsilon subtitle",
        )
        epsilon.suitable_audiences.set([push_limit])
        create_tour(location=epsilon, title="Tour Epsilon")

        gamma = create_location(
            name="Gamma",
            description="Gamma description",
        )
        gamma.suitable_audiences.set([push_limit])
        create_tour(location=gamma, title="Tour Gamma")

        inactive = create_location(
            name="Aardvark",
            description="Should not appear",
            home_feature_order=3,
        )
        create_tour(location=inactive, title="Tour inactive", is_active=False)

        response = self.client.get(reverse("home-featured-routes"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        payload = response.json()

        self.assertEqual(
            [item["name"] for item in payload["routes"]],
            ["Alpha", "Beta", "Delta", "Epsilon"],
        )
        self.assertEqual(payload["routes"][0]["display_name"], "Alpha Ridge")
        self.assertEqual(payload["routes"][0]["summary"], "Alpha description")
        self.assertEqual(
            [item["title"] for item in payload["routes"][0]["suitable_audiences"]],
            ["Người mới", "Trung cấp"],
        )
        self.assertEqual(payload["routes"][1]["summary"], "Beta summary")
        self.assertEqual(payload["routes"][2]["display_name"], "Delta")

        self.assertEqual(
            payload["highlight_audience"]["title"],
            "Người muốn vượt giới hạn",
        )
        self.assertEqual(
            [item["name"] for item in payload["highlight_audience"]["locations"]],
            ["Delta", "Epsilon", "Gamma"],
        )


class HomeMomentsGalleryApiTests(APITestCase):
    def test_home_moments_gallery_returns_all_valid_tour_images_with_tour_context(self):
        active_location = create_location(name="Ta Chi Nhu")
        inactive_location = create_location(name="Pu Ta Leng")

        active_tour = create_tour(location=active_location, title="Bình minh Tà Chì Nhù")
        inactive_tour = create_tour(
            location=inactive_location,
            title="Rừng rêu Putaleng",
            is_active=False,
        )

        first_image = TourImage.objects.create(
            tour=active_tour,
            image_url="https://cdn.example.com/moment-1.jpg",
            caption="Biển mây đầu ngày",
            sort_order=1,
        )
        second_image = TourImage.objects.create(
            tour=inactive_tour,
            image_url="https://cdn.example.com/moment-2.jpg",
            caption="Rừng rêu cổ thụ",
            sort_order=0,
        )
        TourImage.objects.create(
            tour=active_tour,
            caption="Không có URL ảnh nên không được trả về",
            sort_order=2,
        )

        response = self.client.get(reverse("home-moments-gallery"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        payload = response.json()

        self.assertEqual([item["id"] for item in payload["images"]], [second_image.id, first_image.id])
        self.assertEqual(payload["images"][0]["caption"], "Rừng rêu cổ thụ")
        self.assertEqual(payload["images"][0]["tour_title"], "Rừng rêu Putaleng")
        self.assertEqual(payload["images"][0]["location_name"], "Pu Ta Leng")
        self.assertEqual(payload["images"][0]["image_url"], "https://cdn.example.com/moment-2.jpg")
        self.assertIsNone(payload["images"][0]["width"])
        self.assertIsNone(payload["images"][0]["height"])
