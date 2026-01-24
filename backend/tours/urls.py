from django.urls import path

from .views import HotTourListView, LocationListView

urlpatterns = [
    path("tours/hot/", HotTourListView.as_view(), name="hot-tours"),
    path("locations/", LocationListView.as_view(), name="location-list"),
]
