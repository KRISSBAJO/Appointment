from django import template

register = template.Library()

@register.filter(name='if_attr')
def if_attr(value, arg):
    """Returns attribute if condition is True"""
    if arg:
        return value
    return ''
