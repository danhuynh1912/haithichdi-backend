from __future__ import annotations

from datetime import date, timedelta

from ..models import Tour, TourItineraryDay


def get_required_itinerary_day_numbers(tour: Tour) -> list[int]:
    if not tour.start_date or not tour.end_date:
        return []
    if tour.end_date < tour.start_date:
        return []

    # Day 0 is one day before start_date.
    total_days = (tour.end_date - tour.start_date).days + 2
    return list(range(total_days))


def get_itinerary_date_by_day(tour: Tour, day_number: int) -> date | None:
    if not tour.start_date:
        return None
    return tour.start_date + timedelta(days=day_number - 1)


def build_default_day_title(tour: Tour, day_number: int) -> str:
    label = f"Day {day_number}"
    day_date = get_itinerary_date_by_day(tour, day_number)
    if day_date is None:
        return label
    return f"{label} - {day_date.strftime('%d/%m/%Y')}"


def sync_itinerary_days_for_tour(tour: Tour, *, remove_out_of_range: bool = True) -> list[TourItineraryDay]:
    required_numbers = set(get_required_itinerary_day_numbers(tour))
    existing_days = {
        item.day_number: item
        for item in TourItineraryDay.objects.filter(tour=tour).order_by("day_number", "id")
    }

    for day_number in sorted(required_numbers):
        day = existing_days.get(day_number)
        if day is None:
            TourItineraryDay.objects.create(
                tour=tour,
                day_number=day_number,
                title=build_default_day_title(tour, day_number),
            )
            continue
        if not day.title.strip():
            day.title = build_default_day_title(tour, day_number)
            day.save(update_fields=["title"])

    if remove_out_of_range:
        out_of_range_numbers = [number for number in existing_days if number not in required_numbers]
        if out_of_range_numbers:
            TourItineraryDay.objects.filter(tour=tour, day_number__in=out_of_range_numbers).delete()

    return list(TourItineraryDay.objects.filter(tour=tour).order_by("day_number", "id"))
