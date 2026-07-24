from django.contrib import admin

from .models import Blog, Category, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


class CommentInline(admin.TabularInline):
    model = Comment
    fields = ('author', 'text')
    extra = 1

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "category", "datetime_created", "datetime_modified")
    list_filter = ("author", "category", "datetime_created", "datetime_modified")
    search_fields = ("title", "text")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [CommentInline]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'blog', 'is_approved', 'datetime_created')
    list_filter = ('is_approved', 'author', 'datetime_created')
    list_editable = ('is_approved',)
    search_fields = ('text', 'author__username')
    actions = ('approve_comments', 'unapprove_comments')

    @admin.action(description="تأیید نظرات انتخاب‌شده")
    def approve_comments(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f"{updated} نظر تأیید شد.")

    @admin.action(description="لغو تأیید نظرات انتخاب‌شده")
    def unapprove_comments(self, request, queryset):
        updated = queryset.update(is_approved=False)
        self.message_user(request, f"{updated} نظر لغو تأیید شد.")
