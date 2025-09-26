from django.contrib import admin
from .models import BlogPost

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "created_at")
    search_fields = ("title", "slug", "content")
    prepopulated_fields = {"slug": ("title",)}
