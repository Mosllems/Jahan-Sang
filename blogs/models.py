from django.db import models
from config import settings
from django.utils.text import slugify



class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام دسته‌بندی", unique=True)
    slug = models.SlugField(max_length=100, unique=True, allow_unicode=True)

    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


class Blog(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name="نویسنده", related_name="blog_author")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="blogs", verbose_name="دسته‌بندی")
    photo = models.ImageField(upload_to="blog_photos", blank=False, null=False, verbose_name="عکس مقاله")
    title = models.CharField(max_length=200, verbose_name="عنوان مقاله", unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True, verbose_name="اسلاگ")
    text = models.TextField(verbose_name="متن مقاله")
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "مقاله"
        verbose_name_plural = "مقالات"
        ordering = ["-datetime_created"]

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

