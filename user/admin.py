from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from .forms import UserChangeForm, UserCreationForm
from .models import User


class UserAdmin(BaseUserAdmin):
    """
    Assignee : 훈희

    커스텀된 유저 모델을 admin에서 사용하기 위한 내용입니다.

    """

    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ("nickname", "is_admin")
    list_filter = ("is_admin",)
    fieldsets = (
        (None, {"fields": ("nickname", "password")}),
        ("Permissions", {"fields": ("is_admin",)}),
    )

    add_fieldsets = ((None, {"classes": ("wide",), "fields": ("nickname", "password1", "password2")}),)
    search_fields = ("nickname",)
    ordering = ("nickname",)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
