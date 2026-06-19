from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView


urlpatterns = [
    path("", RedirectView.as_view(url="/module-2/", permanent=False)),
    path("module-2/", include("module2.urls")),
    path("admin/", admin.site.urls),
]
