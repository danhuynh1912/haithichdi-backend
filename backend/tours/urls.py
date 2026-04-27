from django.urls import path

from .views import (
    BookingByIdsListView,
    BookingCreateView,
    BookingDetailView,
    HotTourListView,
    HomeFeaturedRoutesView,
    HomeMomentsGalleryView,
    LocationListView,
    RelatedToursListView,
    TourDetailView,
    TourListView,
)

urlpatterns = [
    path("home/featured-routes/", HomeFeaturedRoutesView.as_view(), name="home-featured-routes"),
    path("home/moments-gallery/", HomeMomentsGalleryView.as_view(), name="home-moments-gallery"),
    path("tours/hot/", HotTourListView.as_view(), name="hot-tours"),
    path("tours/", TourListView.as_view(), name="tour-list"),
    path("tours/<int:pk>/", TourDetailView.as_view(), name="tour-detail"),
    path("tours/<int:pk>/related/", RelatedToursListView.as_view(), name="tour-related"),
    path("bookings/", BookingCreateView.as_view(), name="booking-create"),
    path("bookings/by-ids/", BookingByIdsListView.as_view(), name="booking-by-ids"),
    path("bookings/<int:pk>/", BookingDetailView.as_view(), name="booking-detail"),
    path("locations/", LocationListView.as_view(), name="location-list"),
]
