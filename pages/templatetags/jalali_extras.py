"""Template filter that shows dates in the Jalali (Persian / Shamsi) calendar.

    {% load jalali_extras %}
    {{ blog.datetime_modified|jdate }}          ->  1405/08/25
    {{ blog.datetime_modified|jdate:"long" }}   ->  25 آبان 1405
    {{ blog.datetime_modified|jdate:"%Y.%m" }}  ->  1405.08   (any strftime pattern)

Works with both DateTimeField (converted to the project's TIME_ZONE first, so a
post saved at 23:00 UTC doesn't land on the wrong Persian day) and DateField.
"""

import datetime

import jdatetime
from django import template
from django.utils import timezone

register = template.Library()


@register.filter(name="jdate")
def jdate(value, fmt="%Y/%m/%d"):
    if not value:
        return ""

    if isinstance(value, datetime.datetime):
        if timezone.is_aware(value):
            value = timezone.localtime(value)
        value = value.date()
    elif not isinstance(value, datetime.date):
        return value

    jalali = jdatetime.date.fromgregorian(date=value)

    if fmt == "long":
        return f"{jalali.day} {jalali.j_months_fa[jalali.month - 1]} {jalali.year}"
    return jalali.strftime(fmt)
