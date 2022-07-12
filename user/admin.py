from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User as UserModel


class UserAdmin(BaseUserAdmin):
    list_display = (
        "id",
        "nickname",
    )
    list_display_links = ("nickname",)
    list_filter = ("nickname",)
    search_fields = ("nickname",)
    ordering = (
        "id",
        "nickname",
    )

    fieldsets = (
        (
            "info",
            {
                "fields": (
                    "nickname",
                    "password",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_admin",
                    "is_active",
                )
            },
        ),
    )

    filter_horizontal = []

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ("nickname",)
        else:
            return ("nickname",)


admin.site.register(UserModel, UserAdmin)
