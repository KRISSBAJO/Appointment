from django import template

register = template.Library()

@register.filter
def star_rating(value, position):
    try:
        value = float(value)
    except ValueError:
        return ''

    position = int(position)

    if value >= position:
        return "fas fa-star"
    elif value >= position - 0.5:
        return "fas fa-star-half-alt"
    else:
        return "far fa-star"
