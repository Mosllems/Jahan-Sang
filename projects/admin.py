from django.contrib import admin

from projects.models import Project, ProjectCategory, ProjectImage


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    fields = ('image', 'is_cover')
    extra = 4


@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'client', 'location', 'datetime_created', 'datetime_modified')
    list_filter = ('category',)
    search_fields = ('title', 'client', 'location')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProjectImageInline]


@admin.register(ProjectImage)
class ProjectImageAdmin(admin.ModelAdmin):
    list_display = ('project', 'image', 'is_cover', 'datetime_created', 'datetime_modified')
    list_filter = ('project', 'is_cover')
    search_fields = ('project__title',)
    readonly_fields = ('datetime_created', 'datetime_modified')
    list_editable = ('is_cover',)
