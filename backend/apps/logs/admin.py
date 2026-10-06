from apps.logs.models import AppLog
from django.contrib import admin


@admin.register(AppLog)
class AppLogAdmin(admin.ModelAdmin):
    list_display = ("created_at", "level", "app_name", "message")
    list_filter = ("level", "app_name", "created_at")
    search_fields = ("message", "app_name")
    date_hierarchy = "created_at"
    readonly_fields = ("created_at", "app_name", "level", "message", "extra", "trace")

    # Logs are an audit trail: read only in the admin
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
