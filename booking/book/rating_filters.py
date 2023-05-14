from django import template

register = template.Library()

@register.filter
def star_rating(value, index):
    rounded_value = round(value)
    if index <= rounded_value:
        return "fas fa-star"
    elif value - rounded_value >= 0.5 and index == rounded_value + 1:
        return "fas fa-star-half-alt"
    else:
        return "far fa-star"
