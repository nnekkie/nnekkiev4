from django.contrib import admin
from .models import Vendor
# Register your models here.


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display  = ['name', 'created_at', 'created_by']
    search_fields = ['name', 'created_by']
    list_filter = ['created_at', 'created_by']
    ordering = ['name']
    list_per_page = 25
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at']
    fieldsets = (
        (None, {
            'fields': ('name', 'created_by')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('created_at',),
        }),
    )