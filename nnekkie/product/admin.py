from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(ProductAttachment)
class ProductAttachmentAdmin(admin.ModelAdmin):
    list_display = ['product', 'book', 'is_free', 'active', 'description', 'timestamp']
    list_filter = ['is_free', 'active', 'timestamp']
    search_fields = ['product__name', 'book', 'desc']  # Assuming `Product` has a `name` field
  

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'price','timestamp']
    search_fields = ['name', 'price']
    date_hierarchy = 'updated'