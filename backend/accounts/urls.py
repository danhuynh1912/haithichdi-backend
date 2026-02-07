from django.urls import path

from .views import LeaderListView

urlpatterns = [
    path("leaders/", LeaderListView.as_view(), name="leader-list"),
]
