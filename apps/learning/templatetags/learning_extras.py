from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    """
    Look up a value in a dict using an int or str key.
    Handles the mismatch that occurs when JSON stores numeric keys as strings.
    """
    if not isinstance(dictionary, dict):
        return None
    if key in dictionary:
        return dictionary[key]
    # Try string form
    if str(key) in dictionary:
        return dictionary[str(key)]
    return None


@register.filter
def multiply(value, arg):
    try:
        return float(value) * float(arg)
    except (TypeError, ValueError):
        return 0