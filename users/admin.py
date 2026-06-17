from django.contrib import admin

from users.models import User
from django.contrib.auth.models import Permission


@admin.register(User)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "password", "phone", 'get_groups', 'is_staff', 'is_active')
    list_filter = ("email",)
    search_fields = ("phone", "email")

    def get_groups(self, obj):
        return ", ".join([group.name for group in obj.groups.all()])

        get_groups.short_description = "Groups"

@admin.register(Permission)
class PermitionAdmin(admin.ModelAdmin):
    list_display = ("name", "codename")