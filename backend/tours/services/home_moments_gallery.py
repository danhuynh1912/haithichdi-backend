from __future__ import annotations

from django.db.models import Q

from ..models import TourImage


def get_home_moments_gallery_payload() -> dict[str, object]:
    return {
        "images": list(_get_home_moments_gallery_queryset()),
    }


def _get_home_moments_gallery_queryset():
    return (
        TourImage.objects.select_related("tour__location")
        .filter((Q(image__isnull=False) & ~Q(image="")) | Q(image_url__gt=""))
        .order_by("-id")
    )
