from django import template

register = template.Library()

@register.filter
def star_rating(rating, index):
    if rating >= index:
        return 'fas fa-star'
    elif rating >= index - 0.5:
        return 'fas fa-star-half-alt'
    else:
        return 'far fa-star'
