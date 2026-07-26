from django.contrib import admin

from .models import ContactForm


@admin.register(ContactForm)
class ContactFormAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name")
    list_filter = ("first_name",)
    search_fields = ("first_name",)


