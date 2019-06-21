from django.contrib import admin

# Register your models here.
from django.contrib.admin import register

from blog.models import Post, Comment


class CommentInline(admin.StackedInline):
    model = Comment
    extra = 1


@register(Post)
class PostAdmin(admin.ModelAdmin):

    inlines = [CommentInline]
