"""Shared rich-text editor (CKEditor 5) for every long text field in the admin.

The editor looks and works like a word processor, but the content is saved as
Markdown, so templates render it with the ``markdown`` filter
(``{% load markdown_extras %}``).

To give a ModelAdmin the editor on all of its TextFields, mix in
``RichTextAdminMixin``:

    class ProjectAdmin(RichTextAdminMixin, admin.ModelAdmin):
        ...
"""

import os

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models
from django_ckeditor_5.widgets import CKEditor5Widget


class RichTextWidget(CKEditor5Widget):
    def __init__(self, config_name="default", attrs=None):
        super().__init__(config_name=config_name, attrs=attrs)

    def use_required_attribute(self, initial):
        # The real <textarea> is hidden behind the editor; a browser-side
        # "required" check on a hidden field blocks the form from submitting.
        # Django still validates the field on the server.
        return False

    class Media:
        js = [
            # django-ckeditor-5 skips the translation file when "language" is a
            # dict ({"ui": ..., "content": ...}), so load the Persian UI here.
            "django_ckeditor_5/dist/translations/fa.js",
            "js/ckeditor_markdown_paste.js",
        ]


class RichTextAdminMixin:
    """Use the rich-text editor for every TextField of this admin."""

    formfield_overrides = {
        models.TextField: {"widget": RichTextWidget},
    }


class EditorUploadStorage(FileSystemStorage):
    """Keeps images uploaded from the editor in media/editor_uploads/."""

    def __init__(self):
        super().__init__(
            location=os.path.join(settings.MEDIA_ROOT, "editor_uploads"),
            base_url=f"/{settings.MEDIA_URL.strip('/')}/editor_uploads/",
        )
