from django.db import models
from django.utils.text import slugify


class ProjectCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام دسته‌بندی", unique=True)
    slug = models.SlugField(max_length=100, unique=True, allow_unicode=True)

    class Meta:
        verbose_name = "دسته‌بندی پروژه"
        verbose_name_plural = "دسته‌بندی‌های پروژه"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


class Project(models.Model):
    category = models.ForeignKey(ProjectCategory, on_delete=models.PROTECT, related_name='projects', verbose_name="دسته‌بندی")
    title = models.CharField(max_length=200, verbose_name="عنوان پروژه")
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True, verbose_name="اسلاگ")
    description = models.TextField(verbose_name="توضیحات")
    client = models.CharField(max_length=200, verbose_name="مشتری")
    location = models.CharField(max_length=200, verbose_name="مکان")
    datetime_created = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    datetime_modified = models.DateTimeField(auto_now=True, verbose_name="تاریخ ویرایش")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def cover_image(self):
        return self.images.filter(is_cover=True).first() or self.images.first()

    class Meta:
        verbose_name = "پروژه"
        verbose_name_plural = "پروژه‌ها"
        ordering = ['-datetime_created']


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images', verbose_name="پروژه")
    image = models.ImageField(upload_to='project_images/', verbose_name="تصویر")
    is_cover = models.BooleanField(default=False, verbose_name="تصویر کاور")
    datetime_created = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    datetime_modified = models.DateTimeField(auto_now=True, verbose_name="تاریخ ویرایش")

    class Meta:
        verbose_name = "تصویر پروژه"
        verbose_name_plural = "تصاویر پروژه‌ها"
        ordering = ['-datetime_created']