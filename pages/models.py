from django.db import models
from config import settings


class ContactForm(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="یوزر")
    first_name = models.CharField(max_length=250, verbose_name="نام")
    last_name = models.CharField(max_length=250, verbose_name="نام خانوادگی")
    phone_number = models.CharField(max_length=15, verbose_name="شماره تلفن")
    email = models.EmailField(verbose_name="ایمیل")
    datetime_created = models.DateField(auto_now_add=True)
