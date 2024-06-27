from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class CustomUserAdmin(BaseUserAdmin):
    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        return super().get_queryset(request).filter(is_staff=False)

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if request.user.is_staff:
            return True
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if request.user.is_staff and obj is not None and not obj.is_staff:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if request.user.is_staff and obj is not None and not obj.is_staff:
            return True
        return False

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
