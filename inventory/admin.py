from django.contrib import admin

from .models import Stone, StoneCategory, Tool, ToolCategory


@admin.register(StoneCategory)
class StoneCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(ToolCategory)
class ToolCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Stone)
class StoneAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "quantity", "stock_status_display", "origin", "dimensions")
    list_filter = ("category",)
    search_fields = ("name", "origin")
    list_editable = ("quantity",)
    prepopulated_fields = {"slug": ("name",)}

    @admin.display(description="وضعیت موجودی")
    def stock_status_display(self, obj):
        return obj.stock_status_display


@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "quantity", "stock_status_display", "brand", "condition")
    list_filter = ("category", "condition")
    search_fields = ("name", "brand")
    list_editable = ("quantity",)
    prepopulated_fields = {"slug": ("name",)}

    @admin.display(description="وضعیت موجودی")
    def stock_status_display(self, obj):
        return obj.stock_status_display
