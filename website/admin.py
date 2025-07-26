#/website/admin.py

from django.contrib import admin
from .models import Record, Category

# Admin configuration for the Record model
@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'created_at', 'deadline', 'is_priority')
    list_filter = ('category', 'is_priority', 'status_color', 'deadline')
    search_fields = ('title', 'content')
    ordering = ('-created_at',)

# Admin configuration for the Category model
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
