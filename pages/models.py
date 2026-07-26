from django.db import models
from config import settings


class ContactForm(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="یوزر", null=True, blank=True, related_name="contact_messages")
    first_name = models.CharField(max_length=250, verbose_name="نام")
    last_name = models.CharField(max_length=250, verbose_name="نام خانوادگی")
    phone_number = models.CharField(max_length=15, verbose_name="شماره تلفن")
    email = models.EmailField(verbose_name="ایمیل")
    message = models.TextField(verbose_name="پیام")
    datetime_created = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "فرم تماس"
        verbose_name_plural = "فرم تماس ها"
        ordering = ["-datetime_created"]

    def __str__(self):
        return f"Message from {self.first_name} . {self.last_name}"

