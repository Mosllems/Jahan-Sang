from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    mobile_number = models.CharField(max_length=15 , unique=True, blank=False, null=False)

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')


    def __str__(self):
        return self.user.username
