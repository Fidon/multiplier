from django import template
register = template.Library()

@register.filter
def filt_money(value):
    if isinstance(value, float):
        formatted_value = '{:,.2f}'.format(value)
    elif isinstance(value, int):
        formatted_value = '{:,}'.format(value)
    else:
        formatted_value = value
    return formatted_value

@register.filter
def remove_space(value_str):
    if any(char in [' ', '-'] for char in value_str):
        return value_str.replace(' ', '').replace('-', '')
    return value_str