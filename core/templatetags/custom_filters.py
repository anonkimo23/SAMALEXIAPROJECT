from django import template

register = template.Library()

@register.filter
def isdigit(value):
    """
    Verifica si el valor es un número.
    """
    return str(value).isdigit()
