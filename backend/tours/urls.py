from django.urls import path

from .views import HotTourListView, LocationListView, TourListView

urlpatterns = [
    path("tours/hot/", HotTourListView.as_view(), name="hot-tours"),
    path("tours/", TourListView.as_view(), name="tour-list"),
    path("locations/", LocationListView.as_view(), name="location-list"),
]
