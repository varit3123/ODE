from django.contrib import admin

from .models import Application, Profile, Review


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("full_name", "phone", "user")
    search_fields = ("full_name", "phone", "user__username")


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("user", "transport", "start_date", "payment_method", "status", "created_at")
    list_filter = ("status", "transport", "payment_method")
    search_fields = ("user__username", "user__profile__full_name", "comment")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("application", "user", "created_at")
    search_fields = ("text", "user__username", "user__profile__full_name")
