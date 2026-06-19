from django.urls import path

from . import views


app_name = "module2"

urlpatterns = [
    path("", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("cabinet/", views.cabinet_view, name="cabinet"),
    path("request/", views.request_view, name="request"),
    path("admin-panel/", views.admin_view, name="admin"),
    path("logout/", views.logout_view, name="logout"),
]
