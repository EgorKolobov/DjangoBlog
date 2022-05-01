from django.contrib import admin
from .models import Post, Comment

admin.site.register(Post)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'content', 'parent', 'post', 'date_posted', 'id')
    list_filter = ('author', 'content', 'parent', 'post', 'date_posted', 'id')
    search_fields = ('author', 'content', 'parent', 'post', 'date_posted', 'id')
