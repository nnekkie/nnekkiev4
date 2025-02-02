from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(GroupChat)
class GroupChatAdmin(admin.ModelAdmin):
    list_display = ['name', 'description' ,'host','active']
    prepopulated_fields = {"slug": ("name", )}
    
@admin.register(GroupChatMessage)
class GroupChatMessageAdmin(admin.ModelAdmin):
    list_display = ['groupchat', 'sender', 'message' ,'is_read','date']

    