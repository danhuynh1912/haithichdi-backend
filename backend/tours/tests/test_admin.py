from __future__ import annotations

from django.contrib.admin.sites import AdminSite
from django.test import TestCase

from tours.admin import TourAdmin, TourItineraryDayInline
from tours.models import Tour, TourItineraryDay


class TourAdminTests(TestCase):
    def setUp(self):
        self.model_admin = TourAdmin(Tour, AdminSite())

    def test_admin_includes_itinerary_inline(self):
        inline_models = [inline.model for inline in self.model_admin.inlines]
        self.assertIn(TourItineraryDay, inline_models)
        self.assertIn(TourItineraryDayInline, self.model_admin.inlines)

    def test_admin_loads_itinerary_auto_generate_script(self):
        self.assertIn("tours/admin/tour_itinerary_days.js", self.model_admin.media._js)
