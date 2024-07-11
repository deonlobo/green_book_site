# templatetags/custom_filters.py

from django import template
from django.utils.timezone import localtime
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
        print(f"time zone {tz} {localtime(value, tz)}")
        return localtime(value, tz).strftime("%B %d, %Y at %H:%M")
    except pytz.UnknownTimeZoneError:
        return value
