from __future__ import annotations

from django.db.models import Exists, IntegerField, OuterRef, Prefetch, Value, When
from django.db.models.expressions import Case

from ..models import Location, LocationAudience, Tour


def get_home_featured_routes_payload() -> dict[str, object]:
    featured_locations = list(_get_home_featured_locations(limit=4))
    highlight_audience = _get_highlight_audience()

    return {
        "routes": featured_locations,
        "highlight_audience": highlight_audience,
    }


def _get_home_featured_locations(*, limit: int) -> list[Location]:
    return list(_get_active_locations_queryset()[:limit])


def _get_active_locations_queryset():
    active_tours = Tour.objects.filter(location_id=OuterRef("pk"), is_active=True)
    audience_queryset = LocationAudience.objects.order_by("sort_order", "id")
    has_manual_order = Case(
        When(home_feature_order__isnull=False, then=Value(0)),
        default=Value(1),
        output_field=IntegerField(),
    )

    return (
        Location.objects.annotate(has_active_tours=Exists(active_tours))
        .filter(has_active_tours=True)
        .prefetch_related(
            Prefetch("suitable_audiences", queryset=audience_queryset),
        )
        .order_by(has_manual_order, "home_feature_order", "name")
    )


def _get_highlight_audience() -> LocationAudience | None:
    try:
        highlight_audience = LocationAudience.objects.get(
            code=LocationAudience.Code.PUSH_LIMIT
        )
    except LocationAudience.DoesNotExist:
        return None

    highlight_audience.home_locations = list(
        _get_active_locations_queryset().filter(suitable_audiences=highlight_audience)
    )
    return highlight_audience
