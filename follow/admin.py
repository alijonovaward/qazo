from django.contrib import admin

from follow.models import Follow


# Register your models here.
@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('following', 'follower', 'status')
    list_filter = ('following', 'follower', 'status')
    search_fields = ('following', 'follower')