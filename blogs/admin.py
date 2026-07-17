from django.contrib import admin

from .models import Blog, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "category", "datetime_created", "datetime_modified")
    list_filter = ("author", "category", "datetime_created", "datetime_modified")
    search_fields = ("title", "text")
    prepopulated_fields = {"slug": ("title",)}

