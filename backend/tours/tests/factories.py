from __future__ import annotations

from datetime import date
from decimal import Decimal
from uuid import uuid4

from tours.models import Location, LocationAudience, Tour


def create_location(
    name: str | None = None,
    elevation_m: int = 3046,
    **kwargs,
) -> Location:
    return Location.objects.create(
        name=name or f"Ky Quan San {uuid4().hex[:6]}",
        elevation_m=elevation_m,
        **kwargs,
    )


def create_location_audience(
    *,
    code: str = LocationAudience.Code.BEGINNER,
    title: str = "Người mới",
    description: str = "Lộ trình phù hợp để làm quen với trekking.",
    sort_order: int = 0,
) -> LocationAudience:
    audience, _ = LocationAudience.objects.update_or_create(
        code=code,
        defaults={
            "title": title,
            "description": description,
            "sort_order": sort_order,
        },
    )
    return audience


def create_tour(
    *,
    location: Location | None = None,
    title: str = "Chinh phục Ky Quan San",
    summary: str = "",
    description_md: str = "",
    itinerary_md: str = "",
    start_date: date | None = None,
    end_date: date | None = None,
    price: Decimal | None = None,
    max_guests: int = 20,
    is_active: bool = True,
) -> Tour:
    return Tour.objects.create(
        title=title,
        summary=summary,
        description_md=description_md,
        itinerary_md=itinerary_md,
        start_date=start_date,
        end_date=end_date,
        price=price,
        location=location or create_location(),
        max_guests=max_guests,
        is_active=is_active,
    )
