from django import template

register = template.Library()

@register.filter
def to_mb(value):
    try:
        return round(value / 1024.0 / 1024.0, 2)  # Convert bytes to MB and round to 2 decimal places
    except (ValueError, TypeError):
        return 0  # Fallback for invalid values

@register.filter
def dict_key(value, key):
    """
    Retrieve a value from a dictionary by key.
    Example: {{ my_dict|dict_key:"my_key" }}
    """
    try:
        return value[key]
    except (KeyError, TypeError):
        return None

@register.filter
def div(value, arg):
    try:
        return float(value) / float(arg)
    except (ValueError, ZeroDivisionError):
        return 0

@register.filter
def mul(value, arg):
    try:
        return float(value) * float(arg)
    except ValueError:
        return 0