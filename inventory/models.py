from django.db import models
from django.utils.text import slugify


# ---------- shared status logic ----------
STATUS_LABELS = {
    "available": "موجود",
    "limited": "محدود",
    "out": "ناموجود",
}


class InventoryItem(models.Model):
    """Abstract base for anything we keep stock of (stones, tools).
    Availability status is derived automatically from `quantity`."""

    LOW_STOCK_THRESHOLD = 5

    name = models.CharField(max_length=200, verbose_name="نام")
    slug = models.SlugField(max_length=220, unique=True, allow_unicode=True, verbose_name="اسلاگ")
    quantity = models.PositiveIntegerField(default=0, verbose_name="تعداد")
    image = models.ImageField(upload_to="inventory/", blank=True, null=True, verbose_name="تصویر")
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    @property
    def stock_status(self):
        if self.quantity == 0:
            return "out"
        if self.quantity <= self.LOW_STOCK_THRESHOLD:
            return "limited"
        return "available"

    @property
    def stock_status_display(self):
        return STATUS_LABELS[self.stock_status]


# ---------- stones ----------
class StoneCategory(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="نام دسته‌بندی")
    slug = models.SlugField(max_length=120, unique=True, allow_unicode=True) #allow_unicode=True is for persian characters

    class Meta:
        verbose_name = "دسته‌بندی سنگ"
        verbose_name_plural = "دسته‌بندی‌های سنگ"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True) #allow_unicode=True is for persian characters
        super().save(*args, **kwargs)


class Stone(InventoryItem):
    category = models.ForeignKey(StoneCategory, on_delete=models.PROTECT, related_name="stones", verbose_name="دسته‌بندی")
    origin = models.CharField(max_length=150, blank=True, verbose_name="منشأ")
    dimensions = models.CharField(max_length=100, blank=True, verbose_name="ابعاد")
    thickness = models.CharField(max_length=50, blank=True, verbose_name="ضخامت")

    class Meta(InventoryItem.Meta):
        verbose_name = "سنگ"
        verbose_name_plural = "سنگ‌ها"
        ordering = ["-datetime_created"]
        


# ---------- tools ----------
class ToolCategory(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="نام دسته‌بندی")
    slug = models.SlugField(max_length=120, unique=True, allow_unicode=True)

    class Meta:
        verbose_name = "دسته‌بندی ابزار"
        verbose_name_plural = "دسته‌بندی‌های ابزار"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


class Tool(InventoryItem):
    CONDITION_CHOICES = [
        ("good", "سالم"),
        ("repair", "نیاز به تعمیر"),
        ("broken", "خراب"),
    ]

    category = models.ForeignKey(ToolCategory, on_delete=models.PROTECT, related_name="tools", verbose_name="دسته‌بندی")
    brand = models.CharField(max_length=150, blank=True, verbose_name="برند")
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES, default="good", verbose_name="وضعیت سلامت")

    class Meta(InventoryItem.Meta):
        verbose_name = "ابزار"
        verbose_name_plural = "ابزارها"
        ordering = ["-datetime_created"]