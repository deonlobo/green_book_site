# templatetags/custom_filters.py

from django import template
from django.utils.timezone import localtime
from datetime import datetime, timedelta
from django.utils import timezone
import pytz

register = template.Library()

@register.filter
def convert_to_timezone(value, timezone_str):
    """
    Convert a datetime object to a specified timezone.
    :param value: The datetime object
    :param timezone_str: The timezone string (e.g., 'America/Toronto')
    :return: The datetime object converted to the specified timezone
    """
    if value is None:
        return value
    try:
        tz = pytz.timezone(timezone_str)
        return localtime(value, tz).strftime("%B %d, %Y at %H:%M")
    except pytz.UnknownTimeZoneError:
        return value

@register.filter
def trim_text(value, length=15):
    if len(value) > length:
        return value[:length] + '...'
    return value

@register.filter
def is_new_product(created_date):

    if timezone.is_naive(created_date):
        created_date = timezone.make_aware(created_date, timezone.get_current_timezone())

    now = timezone.now()

    return created_date >= now - timedelta(days=1)