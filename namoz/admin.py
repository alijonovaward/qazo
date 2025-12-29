from django.contrib import admin
from .models import Namoz, NamozAction

# Register your models here.
@admin.register(Namoz)
class NamozAdmin(admin.ModelAdmin):
    search_fields = ('user',)
    list_display = ('user', 'bomdod', 'peshin', 'asr', 'shom', 'xufton', 'vitr')

@admin.register(NamozAction)
class NamozActionAdmin(admin.ModelAdmin):
    search_fields = ['user']
    list_display = ['user', 'prayer', 'action', 'old_value', 'new_value', 'created_at']
    list_filter = ['user', 'prayer', 'action', 'created_at']
