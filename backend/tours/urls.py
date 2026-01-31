from django.urls import path

from .views import (
    BookingCreateView,
    HotTourListView,
    LocationListView,
    TourDetailView,
    TourListView,
)

urlpatterns = [
    path("tours/hot/", HotTourListView.as_view(), name="hot-tours"),
    path("tours/", TourListView.as_view(), name="tour-list"),
    path("tours/<int:pk>/", TourDetailView.as_view(), name="tour-detail"),
    path("bookings/", BookingCreateView.as_view(), name="booking-create"),
    path("locations/", LocationListView.as_view(), name="location-list"),
]
