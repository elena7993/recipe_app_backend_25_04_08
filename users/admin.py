from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# 노란줄


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (
            "프로필",
            {
                "fields": (
                    "username",
                    "name",
                    "password",
                    "email",
                    "avatar",
                )
            },
        ),
        (
            ("권한"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            ("중요날짜"),
            {
                "fields": (
                    "last_login",
                    "date_joined",
                ),
            },
        ),
    )
