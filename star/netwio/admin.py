"""Configures view of admin panel."""
from django.contrib import admin

from netwio.models import Comment
from netwio.models import Post

class PostAdmin(admin.ModelAdmin):
    """Configures view of Post model"""
    list_display = ('title', 'user', 'pub_date')

class CommentAdmin(admin.ModelAdmin):
    """Configures view of Comment model"""
    list_display = ('post', 'user', 'pub_date')

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
