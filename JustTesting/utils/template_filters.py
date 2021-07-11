from django.template.defaultfilters import register


@register.filter
def to_int(value):
    return int(value)
