from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['user','product', 'stripe_price']
    date_hierarchy = 'timestamp'