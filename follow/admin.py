from django.contrib import admin

from .models import Permission

@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'status')
    search_fields = ('sender', 'receiver')
    list_filter = ('sender', 'receiver', 'status')

    class Meta:
        unique_together = (('sender', 'receiver'),)