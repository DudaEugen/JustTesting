from django.template.defaultfilters import register


@register.filter
def to_int(value) -> int:
    """
    convert value to int in template.
    """
    return int(value)
