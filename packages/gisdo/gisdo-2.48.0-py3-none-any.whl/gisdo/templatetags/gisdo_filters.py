from django import (
    template,
)


register = template.Library()


@register.filter
def cutspace(value):
    """Фильтр для вырезания пробелов"""
    return value.replace(' ', '')
