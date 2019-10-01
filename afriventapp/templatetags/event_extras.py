from django import template

register = template.Library()


@register.filter(name='range_value')
def range_val(value):
    return range(0,value)