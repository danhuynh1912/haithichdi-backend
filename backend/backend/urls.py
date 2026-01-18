from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

admin.site.site_header = "Haithichdi administration"
admin.site.site_title = "Haithichdi administration"
admin.site.index_title = "Haithichdi administration"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("tours.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
