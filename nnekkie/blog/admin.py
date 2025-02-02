from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(FollowerRequest)
class FollowerAdmin(admin.ModelAdmin):
    list_editable = ['status']
    date_hierarchy = 'date'
    list_display = ['sender', 'receiver','status']
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ['user', 'caption', 'thumbnail', 'views', 'active', 'like_count']
    date_hierarchy = 'date'
    list_filter = ['active']

@admin.register(Comment)
class CommentFilter(admin.ModelAdmin):
    list_display = ['truncated_blog', 'comment', 'active', 'comment_like_count']

    def truncated_blog(self, obj):
        return obj.blog.title[:20]  # Adjust the number to the desired length

    truncated_blog.short_description = 'Blog'
    list_filter = ['date']

@admin.register(ReplyComment)
class ReplyCommentAdmin(admin.ModelAdmin):
    list_editable = ['active']
    list_display = ['user', 'comment', 'reply', 'active']

    date_hierarchy = 'date'