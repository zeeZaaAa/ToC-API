from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("api/", include([
        path("user/", include("src.users.urls")),
        path("masking-data/", include("src.masking_data.urls")),
    ])),
    path("admin/", admin.site.urls),
]
