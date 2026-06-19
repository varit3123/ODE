from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView


urlpatterns = [
    path("", RedirectView.as_view(url="/module-1/", permanent=False)),
    path("module-1/", include("module1.urls")),
    path("admin/", admin.site.urls),
]
