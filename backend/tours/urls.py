from django.urls import path

from .views import HotTourListView

urlpatterns = [
    path("tours/hot/", HotTourListView.as_view(), name="hot-tours"),
]
