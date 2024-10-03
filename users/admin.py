from django.db import models
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _


User = get_user_model()


@admin.register(User)
class UserModelAdmin(UserAdmin):
    list_display = (
        "id",
        "guid",
        "phone",
        "username",
        "full_name",
        "is_active",
        "role",
    )
    list_filter = ("is_staff", "is_superuser", "is_active")
    search_fields = ("phone", "full_name", "guid", "id")
    ordering = ("full_name",)
    fieldsets = (
        (None, {"fields": ("username", "password", "role")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "full_name",
                    "address",
                    "phone",
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": ("is_active", "is_staff", "is_superuser"),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )